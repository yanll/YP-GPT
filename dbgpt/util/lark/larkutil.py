import json
import logging
from typing import Dict

import requests

from dbgpt.extra.cache.redis_cli import RedisClient
from dbgpt.util import envutils

redis_client = RedisClient()


def get_tenant_access_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    headers = {}
    app_id = envutils.getenv("LARK_APP_ID")
    params = {
        'app_id': app_id,
        'app_secret': envutils.getenv("LARK_APP_SK")
    }
    token = ""
    try:
        redis_key = "lark_tenant_access_token_by_app_id_" + app_id
        token: str = redis_client.get(redis_key)
    except Exception as e:
        logging.error("从缓存读取飞书租户令牌失败：", e)
    if token and token != "":
        print("飞书租户令牌缓存读取成功！")
        return {
            'tenant_access_token': token
        }
    else:
        resp = requests.post(url=url, headers=headers, params=params)
        token = resp.json()['tenant_access_token']
        redis_client.set(redis_key, token, 30 * 60)
        print('\n飞书租户令牌返回结果：', resp.json())
        return resp.json()


def get_app_access_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal"
    headers = {}
    params = {
        'app_id': envutils.getenv("LARK_APP_ID"),
        'app_secret': envutils.getenv("LARK_APP_SK")
    }
    resp = requests.post(url=url, headers=headers, params=params)
    print('飞书应用令牌返回结果：', resp.json())
    return resp.json()


def build_headers(token=None):
    if token is None:
        token = get_tenant_access_token()['tenant_access_token']
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json; charset=utf-8'
    }
    return headers


def select_userinfo_batch(token: str = None, open_id: str = None):
    url = 'https://open.feishu.cn/open-apis/contact/v3/users/batch'
    params = {
        "user_id_type": "open_id",
        "user_ids": [open_id]
    }
    resp = requests.request('GET', url=url, headers=build_headers(token), params=params)
    print('用户列表信息返回结果：', resp.json())
    return resp.json()


def select_userinfo(token: str = None, open_id: str = None):
    url = ('https://open.feishu.cn/open-apis/contact/v3/users/{user_id}'.format(user_id=open_id))

    userinfo_str = ""
    redis_key = "lark_userinfo_by_open_id_" + open_id
    try:
        userinfo_str: str = redis_client.get(redis_key)
    except Exception as e:
        logging.error("从缓存读取飞书用户信息失败：", e)
    if userinfo_str and userinfo_str != "":
        print("飞书用户信息缓存读取成功！", open_id)
        rs = json.loads(userinfo_str)
        print("缓存读取的飞书用户详细信息：", rs)
        return rs
    else:
        resp = requests.request('GET', url=url, headers=build_headers(token))
        if resp.status_code != 200:
            logging.error("飞书用户查询接口异常：" + str(resp.status_code))
            return None
        result = resp.json()
        if result["code"] != 0:
            logging.error("飞书用户查询业务异常：" + resp.text)
            return None
        user = result['data']['user']
        name: str = user['name']

        if "email" not in user:
            raise Exception("请开通飞书通讯录获取邮箱权限！" + name)
        if "mobile" not in user:
            raise Exception("请开通飞书通讯录获取手机号码权限！" + name)
        en_name: str = user['en_name']
        email: str = user['email']
        mobile: str = user['mobile']
        if en_name == "":
            en_name = email.split("@")[0]
        userinfo = {
            "open_id": user['open_id'],
            "union_id": user['union_id'],
            "name": name,
            "en_name": en_name,
            "email": email,
            "mobile": mobile
        }
        redis_client.set(redis_key, json.dumps(userinfo), 10 * 60)
        print('\n用户详细信息返回结果：', userinfo)
        return userinfo

# 发送消息
def send_message(receive_id: str, content: Dict, receive_id_type: str = "email", msg_type: str = "text"):
    url = 'https://open.feishu.cn/open-apis/im/v1/messages'
    params = {
        "receive_id_type": receive_id_type
    }
    data = {
        "receive_id": receive_id,
        "msg_type": msg_type,
        "content": json.dumps(content)
    }
    resp = requests.request('POST', url=url, headers=build_headers(), params=params, data=json.dumps(data))
    print('发送消息返回结果：', resp.json())
    return resp.json()


# 发送交互更新卡片
def send_interactive_update_message(token: str, content: Dict):
    url = 'https://open.feishu.cn/open-apis/interactive/v1/card/update'
    data = {
        "token": token,
        "card": content
    }
    resp = requests.request('POST', url=url, headers=build_headers(), data=json.dumps(data))
    print('发送交互更新卡片返回结果：', resp.json())
    return resp.json()
