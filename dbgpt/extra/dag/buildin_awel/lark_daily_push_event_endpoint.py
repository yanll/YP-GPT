import logging
from typing import List, Dict

import requests
from fastapi import FastAPI

from dbgpt.core.awel import DAG, HttpTrigger, MapOperator
from dbgpt.extra.dag.buildin_awel.langgraph.tools.daily_push_message_tool import Dailypushmessagetool
from dbgpt.extra.dag.buildin_awel.lark import card_templates
from dbgpt.util.azure_util import create_azure_llm
from dbgpt.util.lark import lark_message_util  # 导入发送卡片的工具类
from dbgpt.util.lark import larkutil

# Create FastAPI instance
app = FastAPI()

# Instantiate original tool class
daily_push_tool = Dailypushmessagetool()

# 获取访问令牌
tokens = larkutil.get_tenant_access_token()
token = tokens['tenant_access_token']


def get_user_open_id(emails):
    url = 'https://open.feishu.cn/open-apis/contact/v3/users/batch_get_id?user_id_type=open_id'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    data = {
        "emails": emails,
        "include_resigned": True,
        "mobiles": []
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        response_data = response.json()
        # 检查响应数据是否包含所需的结构
        if response_data.get('code') == 0 and 'data' in response_data and 'user_list' in response_data['data']:
            user_list = response_data['data']['user_list']
            user_dict = {}
            for user in user_list:
                if 'email' in user and 'user_id' in user:
                    user_dict[user['email']] = user['user_id']
                else:
                    print(f"Missing 'email' or 'user_id' in user data: {user}")
            return user_dict
        else:
            # 如果响应数据中没有user_list或code不为0，则返回错误信息
            return {'error': 'Invalid response format'}
    else:
        # 请求失败，返回None或错误信息
        return {'error': f'Request failed with status code {response.status_code}'}


emails = ["liangliang.yan@yeepay.com",
          "huaxue.zhang@yeepay.com",
          "chao.huang@yeepay.com",
          "bo.liu-2@yeepay.com",
          "yangsheng.su@yeepay.com"]
#chaoqun.rao@yeepay.com ，shouhong.cao@yeepay.com
result = get_user_open_id(emails)

conv_ids = result


class RequestHandleOperator(MapOperator[None, List[Dict]]):
    llm = None

    def __init__(self, **kwargs):
        self.llm = create_azure_llm()
        super().__init__(**kwargs)

    async def map(self, input_value: None) -> List[Dict]:
        results = []
        for email, conv_id in conv_ids.items():  # 直接遍历字典的键值对
            print(f"Receive conv_id: {conv_id}")
            try:
                result = daily_push_tool._run(conv_id=conv_id)
                results.append(result)
                data = result.get("data", {})
                if not data:
                    logging.error(f"No data returned from _run function for conv_id {conv_id}")
                    continue
                lark_message_util.send_card_message(
                    receive_id=conv_id,
                    content=card_templates.crem_sales_details_content(
                        template_variable={
                            "unlike_callback_event": {
                                "event_type": "unlike",
                                "event_source": "daily_push_message_list_card",
                                "event_data": {
                                    "message": "人员分级销售详情展示"
                                }
                            },
                            "query_str": data["query_str"],
                            "daily_push_message_list": data["list"],
                            "sales_diapaly": data["sales_diapaly"],
                            "value_colour_yesterday_change_rate": data["value_colour_yesterday_change_rate"],
                            "value_colour_weekly_change_rate": data["value_colour_weekly_change_rate"]
                        }
                    )
                )

            except Exception as e:
                logging.error(f"Error occurred while handling daily push event for conv_id {conv_id}: {e}")
                results.append({"conv_id": conv_id, "error": str(e)})
        return results


with DAG("dbgpt_awel_lark_daily_push_event") as dag:
    trigger = HttpTrigger(
        endpoint="/lark_daily_push_event",
        methods="POST",
        request_body=Dict
    )
    map_node = RequestHandleOperator()
    trigger >> map_node
