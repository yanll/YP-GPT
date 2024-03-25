import requests
import json
from dbgpt.util.sutil import decrypt, ak, sk


def get_tenant_access_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    headers = {}
    params = {
        'app_id': ak(),
        'app_secret': sk()
    }
    resp = requests.post(url=url, headers=headers, params=params)
    print('飞书租户令牌返回结果：', resp.json())
    return resp.json()


def get_app_access_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal"
    headers = {}
    params = {
        'app_id': ak(),
        'app_secret': sk()
    }
    resp = requests.post(url=url, headers=headers, params=params)
    print('飞书应用令牌返回结果：', resp.json())
    return resp.json()


def build_headers():
    token = get_tenant_access_token()['tenant_access_token']
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json; charset=utf-8'
    }
    return headers


def send_message(receive_id, text):
    url = 'https://open.feishu.cn/open-apis/im/v1/messages'
    params = {
        "receive_id_type": "email"
    }
    msg = {
        "text": text
    }
    data = {
        "receive_id": receive_id,
        "msg_type": "text",
        "content": json.dumps(msg)
    }
    resp = requests.request('POST', url=url, headers=build_headers(), params=params, data=json.dumps(data))
    print('发送消息返回结果：', resp.json())
    print('消息标识：', resp.json()['data']['message_id'])
    return resp.json()


"""
创建多维表格 
"""


def muti_table_create(name: str, folder_token: str):
    url = 'https://open.feishu.cn/open-apis/bitable/v1/apps'
    data = {
        "name": name,
        "folder_token": folder_token
    }
    resp = requests.request('POST', url=url, headers=build_headers(), params={}, data=json.dumps(data))
    print('多维表格创建返回结果：', resp.json())
    if resp.json().get('code') == 0:
        print('多维表格创建完成：', resp.json()['data'])
    else:
        print('多维表格创建失败：', resp.json())
    return resp.json()


"""
多维表格插入记录 
"""


def muti_table_add_record(app_id, table_id, record):
    url = ('https://open.feishu.cn/open-apis/bitable/v1/apps/{app_id}/tables/{table_id}/records'
           .format(app_id=app_id, table_id=table_id))
    params = {
        "ts": "123456"
    }
    data = json.dumps(record)
    resp = requests.request('POST', url=url, headers=build_headers(), params=params, data=data)
    print('多维表格添加记录返回结果：', resp.json())
    if resp.json().get('code') == 0:
        print('添加记录完成：', resp.json()['data'])
    else:
        print('添加记录失败：', resp.json())
    return resp.json()

# print(get_tenant_access_token())
# print(get_app_access_token())
# send_message("liangliang.yan@yeepay.com", "你好\n\n点点滴滴！")

# muti_table_create("我是自动创建的多维表格", "PPzIfGbCTlPrHpdfXb8ctLAVnVh")
# rec = {
#     "fields": {
#         "需求内容": "多行文本内容"
#     }
# }
# muti_table_add_record("NorvbogbxaCD4VsMrLlcTzv0nTe", "tblG1alED3YxCJua", rec)
