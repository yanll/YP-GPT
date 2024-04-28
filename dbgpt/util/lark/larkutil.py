import json
from typing import Dict

import requests

from dbgpt.util import envutils


def get_tenant_access_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    headers = {}
    params = {
        'app_id': envutils.getenv("LARK_APP_ID"),
        'app_secret': envutils.getenv("LARK_APP_SK")
    }
    resp = requests.post(url=url, headers=headers, params=params)
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


def select_userinfo(token: str = None, email: str = None):
    url = 'https://open.feishu.cn/open-apis/contact/v3/users/batch_get_id'
    params = {
        "user_id_type": "open_id"
    }
    emails = [email]
    data = {
        "emails": emails
    }
    resp = requests.request('POST', url=url, headers=build_headers(token), params=params, data=json.dumps(data))
    print('用户信息返回结果：', resp.json())
    return resp.json()


def select_buildings(token: str = None):
    """建筑列表"""
    url = 'https://open.feishu.cn/open-apis/meeting_room/building/list'
    params = {
        "page_size": "20",
        "page_token": "0",
        "order_by": "name-asc",
        "fields": "*"
    }
    data = {}
    resp = requests.request('POST', url=url, headers=build_headers(token), params=params, data=json.dumps(data))
    print('建筑列表信息返回结果：', resp.json())
    return resp.json()


def select_rooms(token: str = None, building_id: str = None):
    """会议室列表"""
    url = 'https://open.feishu.cn/open-apis/meeting_room/room/list'
    params = {
        "building_id": building_id,
        "page_token": "0",
        "order_by": "name-asc",
        "fields": "*"
    }
    data = {}
    resp = requests.request('POST', url=url, headers=build_headers(token), params=params, data=json.dumps(data))
    print('会议室列表信息返回结果：', resp.json())
    return resp.json()


def select_room_free_busy(token, room_ids, time_min, time_max):
    """会议室列表"""
    url = 'https://open.feishu.cn/open-apis/meeting_room/freebusy/batch_get'
    params = {
        "room_ids": room_ids,
        "time_min": time_min,
        "time_max": time_max
    }
    data = {}
    resp = requests.request('GET', url=url, headers=build_headers(token), params=params)
    print('会议室忙闲返回结果：', resp.json())
    return resp.json()

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
def send_interactive_update_message(token:str, content: Dict):
    url = 'https://open.feishu.cn/open-apis/interactive/v1/card/update'

    data = {
        "token": token,
        "card":content
    }
    resp = requests.request('POST', url=url, headers=build_headers(), data=json.dumps(data))
    print('发送交互更新卡片返回结果：', resp.json())
    return resp.json()

def muti_table_create(name: str, folder_token: str):
    """
    创建多维表格
    """
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


def muti_table_add_record(app_id, table_id, record):
    """
    多维表格插入记录
    """
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


def create_calendar_id(token):
    """创建日历"""
    url = "https://open.feishu.cn/open-apis/calendar/v4/calendars/primary"
    params = {}
    data = {}
    resp = requests.request('POST', url=url, headers=build_headers(token), params=params, data=data)
    print('查询日历标识：', resp.json())
    if resp.json().get('code') == 0:
        print('查询日历标识完成：', resp.json()['data'])
    else:
        print('查询日历标识失败：', resp.json())
    return resp.json()['data']['calendars'][0]['calendar']['calendar_id']


def grant_calendar(token, calendar_id, role, user_open_id):
    """日历授权"""
    url = (
        'https://open.feishu.cn/open-apis/calendar/v4/calendars/{calendar_id}/acls'.format(calendar_id=calendar_id)
    )
    params = {
        "user_id_type": "open_id"
    }
    data = {
        "role": role,
        "scope": {
            "type": "user",
            "user_id": user_open_id
        }
    }
    data = json.dumps(data)
    resp = requests.request('POST', url=url, headers=build_headers(token), params=params, data=data)
    print('日历授权：', resp.json())
    if resp.json().get('code') == 0:
        print('日历授权完成：', resp.json()['data'])
    else:
        print('日历授权失败：', resp.json())
    return resp.json()


def create_calendar(token, calendar_id, record):
    """创建日历"""
    url = (
        'https://open.feishu.cn/open-apis/calendar/v4/calendars/{calendar_id}/events'.format(calendar_id=calendar_id)
    )
    params = {}
    data = json.dumps(record)
    resp = requests.request('POST', url=url, headers=build_headers(token), params=params, data=data)
    print('创建日历返回结果：', resp.json())
    if resp.json().get('code') == 0:
        print('创建日历完成：', resp.json()['data'])
    else:
        print('创建日历失败：', resp.json())
    return resp.json()


def add_calendar_user(token, calendar_id, event_id, record):
    """添加日程用户"""
    url = (
        'https://open.feishu.cn/open-apis/calendar/v4/calendars/{calendar_id}/events/{event_id}/attendees'.format(
            calendar_id=calendar_id, event_id=event_id)
    )
    params = {}
    data = json.dumps(record)
    resp = requests.request('POST', url=url, headers=build_headers(token), params=params, data=data)
    print('添加用户返回结果：', resp.json())
    if resp.json().get('code') == 0:
        print('添加用户完成：', resp.json()['data'])
    else:
        print('添加用户失败：', resp.json())
    return resp.json()


def add_calendar_room(token, calendar_id, event_id, record):
    """添加日程用户"""
    url = (
        'https://open.feishu.cn/open-apis/calendar/v4/calendars/{calendar_id}/events/{event_id}/attendees'.format(
            calendar_id=calendar_id, event_id=event_id)
    )
    params = {}
    data = json.dumps(record)
    resp = requests.request('POST', url=url, headers=build_headers(token), params=params, data=data)
    print('添加会议室返回结果：', resp.json())
    if resp.json().get('code') == 0:
        print('添加会议室完成：', resp.json()['data'])
    else:
        print('添加会议室失败：', resp.json())
    return resp.json()
