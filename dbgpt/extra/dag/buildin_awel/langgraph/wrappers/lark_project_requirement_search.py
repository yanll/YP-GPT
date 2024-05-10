import requests
import json
import datetime
import json
import time
#from pypinyin import pinyin, lazy_pinyin
import requests
from datetime import datetime
from dbgpt.extra.dag.buildin_awel.lark import card_templates
from dbgpt.util import envutils
from dbgpt.util.lark import lark_card_util, larkutil


def create_requirement_search_for_lark_project(
        token,
        requirement_create_name,
        project_key: str,
        union_id,
        business_value,
        priority_value
):
    rs = requirement_search(
        project_key=project_key,
        requirement_create_name = requirement_create_name,
        union_id=union_id,
        business_value=business_value,
        priority_value=priority_value,

    )
    print("需求查询结果:", rs)
    print("开始更新需求查询卡片")

    return rs



def get_project_app_token():
    url = 'https://project.feishu.cn/bff/v2/authen/plugin_token'
    headers = {'Content-Type': 'application/json'}
    data = {
        "plugin_id": envutils.getenv("LARK_PROJECT_PLUGIN_ID"),
        "plugin_secret": envutils.getenv("LARK_PROJECT_PLUGIN_SECRET"),
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

def get_name_cn(union_id):
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
            return response_data['data'][0].get('name_cn')
        else:
            return "No name_cn found in the response."
    except Exception as e:
        return str(e)



# def chinese_name_to_email(requirement_create_name):
#     pinyin_name = ''.join(lazy_pinyin(requirement_create_name))
#     # 提取姓和名的拼音
#     last_name = lazy_pinyin(requirement_create_name[0])[0]
#     first_name = pinyin_name[len(last_name):]
#     # 构建邮箱格式
#     email = first_name.lower() + '.' + last_name.lower() + '@yeepay.com'
#     return email


# def get_search_user_key(requirement_create_name):
#     url = 'https://project.feishu.cn/open_api/user/query'
#     headers = {
#         'X-PLUGIN-TOKEN': get_project_app_token(),
#         'Content-Type': 'application/json'
#     }
#     data = {
#         "user_keys": [chinese_name_to_email(requirement_create_name)]
#     }
#
#     try:
#         response = requests.post(url, headers=headers, data=json.dumps(data))
#         response_data = response.json()
#         if response_data and 'data' in response_data and len(response_data['data']) > 0:
#             search_id = response_data['data'][0].get('user_keys')
#             print("查询所得的用户key为:", search_id)  # 打印用户键
#             return search_id
#
#         else:
#             return "No user_keys found in the response."
#     except Exception as e:
#         return str(e)



def requirement_search(union_id,requirement_create_name,project_key, business_value=None, priority_value=None):
    global priority_label
    #acc = json.dumps(get_search_user_key(requirement_create_name))[1:-1]
    #print("用户账户的id",acc)
    url = 'https://project.feishu.cn/open_api/' + project_key + '/work_item/story/search/params'
    headers = {
        'X-PLUGIN-TOKEN': get_project_app_token(),
        'X-USER-KEY': get_user_key(union_id),
        #'X-USER-KEY': "7355229159460749315",
        'Content-Type': 'application/json'
    }
    data = {
        "search_group": {
            "conjunction": "AND",
            "search_params": [
                {
                    "param_key": "people",
                    "value": ["7355229159460749315"],
                    "operator": "HAS ANY OF"
                },
                {
                "param_key":"business",
                "value":[business_value],
                "operator":"HAS ANY OF"
                },
                {
                "param_key":"priority",
                "value":[priority_value],
                "operator":"HAS ANY OF"
                }
            ]
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    result = response.json()

    extracted_data = []
    for item in result.get('data', []):
        extracted_item = {
            "name": item.get('name', ''),
            "exp_time": None,
            "priority_label": '',
            "business_id": '',
            "start_time": None,
            "owner": get_name_cn(union_id)
        }
        fields = item.get('fields', [])
        for field in fields:
            if field['field_key'] == 'exp_time':
                extracted_item['exp_time'] = timestamp_to_date(field['field_value'])
            elif field['field_key'] == 'priority':
                extracted_item['priority_label'] = field['field_value']['label']
                priority_label = field['field_value']['label']
                print("紧急程度是：", priority_label)
            elif field['field_key'] == 'business':
                extracted_item['business_id'] = field['field_value']
            elif field['field_key'] == 'start_time':
                extracted_item['start_time'] = timestamp_to_date(field['field_value'])
        extracted_data.append(extracted_item)

    return extracted_data,priority_label




def timestamp_to_date(timestamp):
    # 将时间戳转换为指定格式日期
    return datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d')



