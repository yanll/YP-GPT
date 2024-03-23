import requests
import json
import uuid
from dbgpt.util.sutil import decrypt, ak, sk


def get_tenant_access_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    headers = {}
    params = {
        'app_id': ak(),
        'app_secret': sk()
    }
    resp = requests.post(url=url, headers=headers, params=params)
    print('飞书令牌返回结果：', resp.json())
    return resp.json()


def send_message(receive_id, text):
    token = get_tenant_access_token()['tenant_access_token']
    url = 'https://open.feishu.cn/open-apis/im/v1/messages'
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json; charset=utf-8'
    }
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
    resp = requests.request('POST', url=url, headers=headers, params=params, data=json.dumps(data))
    print('发送消息返回结果：', resp.json())
    print('消息标识：', resp.json()['data']['message_id'])
    return resp.json()
