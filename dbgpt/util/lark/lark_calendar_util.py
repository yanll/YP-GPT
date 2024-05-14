import json

import requests

from dbgpt.util import consts
from dbgpt.util.lark.larkutil import build_headers


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
    resp = requests.request('POST', url=url, headers=build_headers(token), params=params, data=json.dumps(data),
                            timeout=consts.request_time_out)
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
    resp = requests.request('POST', url=url, headers=build_headers(token), params=params, data=json.dumps(data),
                            timeout=consts.request_time_out)
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
    resp = requests.request('GET', url=url, headers=build_headers(token), params=params,
                            timeout=consts.request_time_out)
    print('会议室忙闲返回结果：', resp.json())
    return resp.json()


def create_calendar_id(token):
    """创建日历"""
    url = "https://open.feishu.cn/open-apis/calendar/v4/calendars/primary"
    params = {}
    data = {}
    resp = requests.request('POST', url=url, headers=build_headers(token), params=params, data=data,
                            timeout=consts.request_time_out)
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
    resp = requests.request('POST', url=url, headers=build_headers(token), params=params, data=data,
                            timeout=consts.request_time_out)
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
    resp = requests.request('POST', url=url, headers=build_headers(token), params=params, data=data,
                            timeout=consts.request_time_out)
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
    resp = requests.request('POST', url=url, headers=build_headers(token), params=params, data=data,
                            timeout=consts.request_time_out)
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
    resp = requests.request('POST', url=url, headers=build_headers(token), params=params, data=data,
                            timeout=consts.request_time_out)
    print('添加会议室返回结果：', resp.json())
    if resp.json().get('code') == 0:
        print('添加会议室完成：', resp.json()['data'])
    else:
        print('添加会议室失败：', resp.json())
    return resp.json()
