from typing import List, Dict
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dbgpt.extra.dag.buildin_awel.langgraph.tools.daily_push_message_tool import Dailypushmessagetool
from dbgpt.core.awel import DAG, HttpTrigger, MapOperator
from dbgpt.extra.dag.buildin_awel.lark import card_templates
from dbgpt.util.azure_util import create_azure_llm
from dbgpt.util.lark import lark_message_util  # 导入发送卡片的工具类
import json
import requests
from dbgpt.util.lark import larkutil

#Create FastAPI instance
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
                # 检查每个用户字典中是否存在'email'和'user_id'
                if 'email' in user and 'user_id' in user:
                    user_dict[user['email']] = user['user_id']
                else:
                    # 如果缺少'email'或'user_id'，可以记录日志或抛出异常
                    print(f"Missing 'email' or 'user_id' in user data: {user}")
            return user_dict
        else:
            # 如果响应数据中没有user_list或code不为0，则返回错误信息
            return {'error': 'Invalid response format'}
    else:
        # 请求失败，返回None或错误信息
        return {'error': f'Request failed with status code {response.status_code}'}

#示例用法
emails = ["liangliang.yan@yeepay.com","huaxue.zhang@yeepay.com"]
result = get_user_open_id(emails)

# 现在result是一个包含所有邮箱和对应conv_id的字典
conv_ids = result

print(conv_ids)  # 打印出包含字典的列表
# Predefined conv_id list
# conv_ids = [
#     {'huaxue.zhang@yeepay.com': 'ou_9d42bb88ec8940baf3ad183755131881'},
#     {'liangliang.yan@yeepay.com': 'ou_a22698cffd738d7851ef30f5dad1a06c'},
#     #{'yangsheng.su@yeepay.com': 'ou_079964d3b15f58fc330058a629b8ed41'},
#     #{'bo.liu-2@yeepay.com': 'ou_850210efe332c6e50256b21b29832f1f'}
# ]

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

# import requests
#
# # 请求的数据，根据你的接口需要进行相应的设置
# data = {
#     }
#
# # 发送 POST 请求
# response = requests.post("http://172.31.91.206:5670/api/v1/awel/trigger/lark_daily_push_event", json=data)
#
# # 输出响应结果
# print(response.status_code)
# print(response.json())

# from fastapi import FastAPI
# import requests
# import logging
# from typing import List, Dict
#
# # Create FastAPI instance
# app = FastAPI()
#
# # Instantiate original tool class
# daily_push_tool = Dailypushmessagetool()
#
# # 获取访问令牌
# tokens = larkutil.get_tenant_access_token()
# token = tokens['tenant_access_token']
#
# def get_user_open_id(emails):
#     url = 'https://open.feishu.cn/open-apis/contact/v3/users/batch_get_id?user_id_type=open_id'
#     headers = {
#         'Content-Type': 'application/json',
#         'Authorization': f'Bearer {token}'
#     }
#     data = {
#         "emails": emails,
#         "include_resigned": True,
#         "mobiles": []
#     }
#
#     response = requests.post(url, headers=headers, json=data)
#     if response.status_code == 200:
#         response_data = response.json()
#         if response_data.get('code') == 0 and 'data' in response_data and 'user_list' in response_data['data']:
#             user_list = response_data['data']['user_list']
#             user_dict = {}
#             for user in user_list:
#                 if 'email' in user and 'user_id' in user:
#                     user_dict[user['email']] = user['user_id']
#                 else:
#                     logging.error(f"Missing 'email' or 'user_id' in user data: {user}")
#             return user_dict
#         else:
#             logging.error("Invalid response format")
#     else:
#         logging.error(f"Request failed with status code {response.status_code}")
#
# def process_daily_push(conv_ids):
#     results = []
#     for conv_info in conv_ids:
#         email, conv_id = list(conv_info.items())[0]  # 获取字典中的邮箱和conv_id
#         print(f"Receive conv_id: {conv_id}")
#         try:
#             result = daily_push_tool._run(conv_id=conv_id)
#             results.append(result)
#             data = result.get("data", {})
#             if not data:
#                 logging.error(f"No data returned from _run function for conv_id {conv_id}")
#                 continue
#             lark_message_util.send_card_message(
#                 receive_id=conv_id,
#                 content=card_templates.crem_sales_details_content(
#                     template_variable={
#                         "unlike_callback_event": {
#                             "event_type": "unlike",
#                             "event_source": "daily_push_message_list_card",
#                             "event_data": {
#                                 "message": "人员分级销售详情展示"
#                             }
#                         },
#                         "query_str": data["query_str"],
#                         "daily_push_message_list": data["list"],
#                         "sales_diapaly": data["sales_diapaly"],
#                         "value_colour_yesterday_change_rate": data["value_colour_yesterday_change_rate"],
#                         "value_colour_weekly_change_rate": data["value_colour_weekly_change_rate"]
#                     }
#                 )
#             )
#
#         except Exception as e:
#             logging.error(f"Error occurred while handling daily push event for conv_id {conv_id}: {e}")
#             results.append({"conv_id": conv_id, "error": str(e)})
#     return results
#
# @app.post("/process_daily_push")
# async def trigger_daily_push():
#     emails = ["huaxue.zhang@yeepay.com", "liangliang.yan@yeepay.com","bo.liu-2@yeepay.com"]
#     conv_ids = [get_user_open_id(emails)]
#     return process_daily_push(conv_ids)
