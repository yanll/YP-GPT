import datetime
import json

import requests

from dbgpt.extra.dag.buildin_awel.lark import card_templates
from dbgpt.util.lark import lark_card_util


def create_requirement_for_lark_project(project_key: str, union_id, name, business_value, priority_value,
                                        expected_time):
    rs = create_and_send_work_item(
        project_key=project_key,
        union_id=union_id,
        name=name,
        business_value=business_value,
        priority_value=priority_value,
        expected_time=expected_time
    )
    card = {
        "toast": {
            "type": "info",
            "content": "温馨提示",
            "i18n": {
                "zh_cn": "信息已提交，请查看结果！",
                "en_us": "submitted"
            }
        },
        "card": {
            "type": "template",
            "data": card_templates.create_requirement_card_content(
                template_variable={
                    "card_metadata": {
                        "card_name": "requirement_collect"
                    },
                    "requirement_content": "-",
                    "industry_line": "",
                    "expected_completion_date": "",
                    "emergency_level": ""
                }
            )
        }
    }
    return card


def get_project_app_token():
    url = 'https://project.feishu.cn/bff/v2/authen/plugin_token'
    headers = {'Content-Type': 'application/json'}
    data = {
        "plugin_id": "MII_6620D4D5830B401C",
        "plugin_secret": "249E74635DFA34E434B14EF3D7CA164D",
        "type": 0
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()["data"]["token"]


def get_user_key(union_id):
    url = 'https://project.feishu.cn/open_api/user/query'
    headers = {
        'X-PLUGIN-TOKEN': get_project_app_token(),
        'Content-Type': 'application/json'
    }
    data = {
        "out_ids": [union_id]
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response_data = response.json()
        if response_data and 'data' in response_data and len(response_data['data']) > 0:
            return response_data['data'][0].get('user_key')
        else:
            return "No user key found in the response."
    except Exception as e:
        return str(e)


def get_template_id(project_key, union_id):
    # url = 'https://project.feishu.cn/open_api/' + api_path + '/ template_list / story'
    url = 'https://project.feishu.cn/open_api/' + project_key + '/template_list/story'

    headers = {'X-PLUGIN-TOKEN': get_project_app_token(),
               'X-USER-KEY': get_user_key(union_id)}

    try:
        response = requests.get(url, headers=headers)
        response_data = response.json()
        if response_data and 'data' in response_data and len(response_data['data']) > 0:
            return response_data['data'][0].get('template_id')
        else:
            return "No template_id found in the response."
    except Exception as e:
        return str(e)


def create_and_send_work_item(project_key, union_id, name, business_value, priority_value, expected_time):
    # 直接在函数内定义 API URL 和 headers
    url = 'https://project.feishu.cn/open_api/' + project_key + '/work_item/create'
    headers = {
        'X-PLUGIN-TOKEN': get_project_app_token(),
        'X-USER-KEY': get_user_key(union_id),
        'X-IDEM-UUID': '',
        'Content-Type': 'application/json'
    }

    # 将日期对象转换为毫秒级时间戳
    timestamp = int(datetime.datetime.strptime(expected_time.replace(" +0800", ""), "%Y-%m-%d").timestamp() * 1000)
    # 构建请求的数据结构
    emergency_level_options: list = lark_card_util.card_options_for_requirement_emergency_level()
    data = {
        "work_item_type_key": "story",
        "template_id": get_template_id(project_key, union_id),
        "name": name,
        "field_value_pairs": [
            {
                "field_key": "business",
                "field_value": business_value,
                "field_type_key": "business",
                "field_alias": "business"

            },

            {
                "field_key": "priority",
                "field_value": {
                    "label": lark_card_util.get_text_by_value_from_options(priority_value, emergency_level_options),
                    "value": priority_value
                }
            },
            {
                "field_key": "exp_time",
                "field_value": timestamp,
                "field_type_key": "date",
                "field_alias": "exp_time",
                "help_description": ""
            }
        ]
    }
    # 发送 POST 请求
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print("飞书项目需求创建结果：", response.json())
    return response.json()
