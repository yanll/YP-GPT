from typing import Dict

import requests
import json
import datetime


def handle_lark_callback(input_body: Dict):
    form_value = input_body['event']['action']['form_value']

    result = create_and_send_work_item(
        name=form_value['requirement_content'],
        priority_value=form_value['emergency_level'],
        expected_time=form_value['expected_completion_date']
    )
    print("飞书回调执行结果：", result)

    pass


rs = {
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
        "data": {
            "template_id": "AAqkjMFhiuVwF", "template_version_name": "1.0.10",
            "template_variable": {
                "requirement_content": "-",
                "expected_completion_date": "",
                "emergency_level": ""
            }
        }
    }
}


def get_project_app_token():
    url = 'https://project.feishu.cn/bff/v2/authen/plugin_token'
    headers = {'Content-Type': 'application/json'}
    data = {
        "plugin_id": "MII_6620D4D5830B401C",
        "plugin_secret": "249E74635DFA34E434B14EF3D7CA164D",
        "type": 1
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()["data"]["token"]


def create_and_send_work_item(name, priority_value, expected_time):
    # 直接在函数内定义 API URL 和 headers
    url = 'https://project.feishu.cn/open_api/ypgptapi/work_item/create'
    headers = {
        'X-PLUGIN-TOKEN': get_project_app_token(),
        'X-USER-KEY': '7355229159460749315',
        'X-IDEM-UUID': '',
        'Content-Type': 'application/json'
    }
    # 将 label 映射到对应的 value
    value_to_label = {
        "0": "P0",
        "1": "P1",
        "2": "P2",
        "99": "待定"
    }
    # 将日期对象转换为毫秒级时间戳
    timestamp = int(datetime.datetime.strptime(expected_time.replace(" +0800", ""), "%Y-%m-%d").timestamp() * 1000)
    # 构建请求的数据结构
    data = {
        "work_item_type_key": "story",
        "template_id": 979341,
        "name": name,
        "field_value_pairs": [
            {
                "field_key": "priority",
                "field_value": {
                    "label": value_to_label[priority_value],
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
    return response.json()
