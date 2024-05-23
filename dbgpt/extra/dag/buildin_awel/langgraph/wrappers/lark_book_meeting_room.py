# from dbgpt.util.lark import ssoutil, larkutil, lark_calendar_util
# import json
# import requests
# from dbgpt.util import consts
# from dbgpt.util.lark.larkutil import build_headers
#
# tokens = larkutil.get_tenant_access_token()
# token = tokens['tenant_access_token']
#
#
# def select_buildings(token: str):
#     """建筑列表"""
#     url = 'https://open.feishu.cn/open-apis/meeting_room/building/list'
#     params = {
#         "page_size": "20",
#         "page_token": "0",
#         "order_by": "name-asc",
#         "fields": "*"
#     }
#     data = {}
#     headers = build_headers(token)
#
#     resp = requests.post(url=url, headers=headers, params=params, data=json.dumps(data),
#                          timeout=consts.request_time_out)
#     print('建筑列表信息返回结果：', resp.json())
#     return resp.json()
#
#
# def select_room_free_busy(open_id, token, room_ids, time_min, time_max):
#     """会议室列表"""
#     url = 'https://open.feishu.cn/open-apis/meeting_room/freebusy/batch_get'
#     params = {
#         "room_ids": room_ids,
#         "time_min": time_min,
#         "time_max": time_max
#     }
#     data = {}
#     resp = requests.request('GET', url=url, headers=build_headers(token), params=params,
#                             timeout=consts.request_time_out)
#     print('会议室忙闲返回结果：', resp.json())
#     return resp.json()
#
#
# def create_calendar_id(token):
#     """创建日历"""
#     url = "https://open.feishu.cn/open-apis/calendar/v4/calendars/primary"
#     params = {}
#     data = {}
#     resp = requests.request('POST', url=url, headers=build_headers(token), params=params, data=data,
#                             timeout=consts.request_time_out)
#     print('查询日历标识：', resp.json())
#     if resp.json().get('code') == 0:
#         print('查询日历标识完成：', resp.json()['data'])
#     else:
#         print('查询日历标识失败：', resp.json())
#     result = resp.json()['data']['calendars'][0]['calendar']['calendar_id']
#     print(result)
#     return resp.json()['data']['calendars'][0]['calendar']['calendar_id']
#
#
# def grant_calendar(token, calendar_id, open_id):
#     """日历授权"""
#     # calendar_id = create_calendar_id
#     # user_open_id = "ou_9d42bb88ec8940baf3ad183755131881"
#     user_open_id = open_id
#     url = (
#         'https://open.feishu.cn/open-apis/calendar/v4/calendars/{calendar_id}/acls'.format(calendar_id=calendar_id)
#     )
#     params = {
#         "user_id_type": "open_id"
#     }
#     data = {
#         "role": "writer",
#         "scope": {
#             "type": "user",
#             "user_id": user_open_id
#         }
#     }
#     data = json.dumps(data)
#     resp = requests.request('POST', url=url, headers=build_headers(token), params=params, data=data,
#                             timeout=consts.request_time_out)
#     print('日历授权：', resp.json())
#     if resp.json().get('code') == 0:
#         print('日历授权完成：', resp.json()['data'])
#     else:
#         print('日历授权失败：', resp.json())
#     return resp.json()
#
#
# def create_calendar(token, calendar_id, time_min, time_max):
#     """创建日历"""
#     title = "我的日程"
#     summary = title
#     description = title
#     calendar = lark_calendar_util.create_calendar(token, calendar_id, {
#         "summary": summary,
#         "description": description,
#         "need_notification": "false",
#         "start_time": {
#             "timestamp": str(time_min),
#             "timezone": "Asia/Shanghai"
#         },
#         "end_time": {
#             "timestamp": str(time_max),
#             "timezone": "Asia/Shanghai"
#         },
#         "visibility": "default",
#         "attendee_ability": "can_modify_event",
#         "free_busy_status": "busy",
#         "color": 0,
#         "reminders": [
#             {
#                 "minutes": 5
#             }
#         ]
#     })
#     #     url = (
#     #     'https://open.feishu.cn/open-apis/calendar/v4/calendars/{calendar_id}/events'.format(calendar_id=calendar_id)
#     # )
#     # params = {}
#     # data = json.dumps(record)
#     # resp = requests.request('POST', url=url, headers=build_headers(token), params=params, data=data,
#     #                         timeout=consts.request_time_out)
#     # print('创建日历返回结果：', resp.json())
#     # if resp.json().get('code') == 0:
#     #     print('创建日历完成：', resp.json()['data'])
#     # else:
#     #     print('创建日历失败：', resp.json())
#     return calendar
#
#
# def add_calendar_user(token, calendar_id, event_id, record):
#     """添加日程用户"""
#     url = (
#         'https://open.feishu.cn/open-apis/calendar/v4/calendars/{calendar_id}/events/{event_id}/attendees'.format(
#             calendar_id=calendar_id, event_id=event_id)
#     )
#     params = {}
#     data = json.dumps(record)
#     resp = requests.request('POST', url=url, headers=build_headers(token), params=params, data=data,
#                             timeout=consts.request_time_out)
#     print('添加用户返回结果：', resp.json())
#     if resp.json().get('code') == 0:
#         print('添加用户完成：', resp.json()['data'])
#     else:
#         print('添加用户失败：', resp.json())
#     return resp.json()
#
#
# def add_calendar_room(token, calendar_id, event_id, record):
#     """添加日程用户"""
#     url = (
#         'https://open.feishu.cn/open-apis/calendar/v4/calendars/{calendar_id}/events/{event_id}/attendees'.format(
#             calendar_id=calendar_id, event_id=event_id)
#     )
#     params = {}
#     data = json.dumps(record)
#     resp = requests.request('POST', url=url, headers=build_headers(token), params=params, data=data,
#                             timeout=consts.request_time_out)
#     print('添加会议室返回结果：', resp.json())
#     if resp.json().get('code') == 0:
#         print('添加会议室完成：', resp.json()['data'])
#     else:
#         print('添加会议室失败：', resp.json())
#     return resp.json()
#
#
# ## 获取租户访问令牌
# # room_ids=["omm_4a260a86bc05a2d7dbb901c53bf5bc92"
# #           ],
# # time_min="2024-05-22T00:00:00+08:00",
# # # time_max="2024-05-22T23:30:00+08:00"
# #
# # c  =  select_room_free_busy(token_str, room_ids, time_min, time_max)
# # print("结果",c)
#
#
# # # 获取建筑列表信息并打印
# # if token_str:
# #     buildings = select_buildings(token_str)
# #     print(buildings)
# # else:
# #     print("无法获取有效的租户令牌")
# calendar_id = create_calendar_id(token)
# a= grant_calendar(token, calendar_id, "ou_9d42bb88ec8940baf3ad183755131881")
# time_min = "2024-08-20T10:30:00+08:00"
# time_max = "2024-08-20T11:00:00+08:00"
# b = create_calendar(token, calendar_id,time_min,time_max)
#
#
from datetime import datetime

from dbgpt.util.lark import lark_calendar_util, larkutil


def test_create_calendar(room_id,grant_user_open_id,start_times,end_times):
    # omm_4a260a86bc05a2d7dbb901c53bf5bc92 敢干
    # omm_1898ce77b933009c84cc999a93aeefc4 敢败
    #room_id = "omm_4a260a86bc05a2d7dbb901c53bf5bc92"
    #grant_user_open_id = "ou_9d42bb88ec8940baf3ad183755131881"
    summary = "我的日程"
    description = "我的日程"
    start_time = int(datetime.strptime(start_times, "%Y-%m-%d %H:%M:%S").timestamp())
    end_time = int(datetime.strptime(end_times, "%Y-%m-%d %H:%M:%S").timestamp())

    token = larkutil.get_tenant_access_token()['tenant_access_token']
    calendar_id = lark_calendar_util.create_calendar_id(token=token)
    lark_calendar_util.grant_calendar(token, calendar_id, "writer", grant_user_open_id)

    calendar = lark_calendar_util.create_calendar(token, calendar_id, {
        "summary": summary,
        "description": description,
        "need_notification": "false",
        "start_time": {
            "timestamp": str(start_time),
            "timezone": "Asia/Shanghai"
        },
        "end_time": {
            "timestamp": str(end_time),
            "timezone": "Asia/Shanghai"
        },
        "visibility": "default",
        "attendee_ability": "can_modify_event",
        "free_busy_status": "busy",
        "color": 0,
        "reminders": [
            {
                "minutes": 5
            }
        ]
    })

    event_id = calendar['data']['event']['event_id']

    lark_calendar_util.add_calendar_user(token, calendar_id, event_id, {
        "attendees": [
            {
                "type": "user",
                "is_optional": "true",
                "user_id": grant_user_open_id
            }
        ],
        "need_notification": "false",
        "is_enable_admin": "false",
        "add_operator_to_attendee": "true"
    })
    lark_calendar_util.add_calendar_room(token, calendar_id, event_id, {
        "attendees": [
            {
                "type": "resource",
                "room_id": room_id
            }
        ],
        "need_notification": "false",
        "is_enable_admin": "false",
        "add_operator_to_attendee": "true"
    })

