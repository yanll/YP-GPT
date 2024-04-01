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

token = get_tenant_access_token()['tenant_access_token']

# select_buildings(token)
# 建筑信息返回结果： {'code': 0, 'data': {'buildings': [{'building_id': 'omb_2cbd7aac59a2292a577547e6d5ef6300', 'country_id': '1814991', 'description': '', 'district_id': '1816670', 'floors': ['F10', 'F23', 'F25'], 'name': '万通中心D座'}, {'building_id': 'omb_db99b4d2a2151bdd21a8461dd03176c2', 'country_id': '1814991', 'description': '', 'district_id': '7111347337074589700', 'floors': ['F'], 'name': '上海'}, {'building_id': 'omb_3840149beda9b7641bd923563316462b', 'country_id': '1814991', 'description': '', 'district_id': '7111347337074589700', 'floors': ['F'], 'name': '分公司'}, {'building_id': 'omb_25d59771f6bca6b59c16c2dd41d1bc6d', 'country_id': '1814991', 'description': '', 'district_id': '7111347337074589700', 'floors': ['F'], 'name': '四川'}, {'building_id': 'omb_7bfc29e767c8b28a832b96ec61b67418', 'country_id': '1814991', 'description': '', 'district_id': '7111347337074589700', 'floors': ['F'], 'name': '山东'}, {'building_id': 'omb_1aeb63f4a74a81a9e22e57f4e41247d2', 'country_id': '1814991', 'description': '', 'district_id': '7111347337074589700', 'floors': ['F'], 'name': '广州'}, {'building_id': 'omb_91121dc669fb7f1301ffa9809c3e8718', 'country_id': '1814991', 'description': '', 'district_id': '7111347337074589700', 'floors': ['F'], 'name': '河南'}, {'building_id': 'omb_448e273409ba89d50e84f46099e6977a', 'country_id': '1814991', 'description': '', 'district_id': '7111347337074589700', 'floors': ['F'], 'name': '浙江'}, {'building_id': 'omb_b90acf40d9e66d042927986e405389f2', 'country_id': '1814991', 'description': '', 'district_id': '7111347337074589700', 'floors': ['F'], 'name': '深圳'}], 'has_more': False}, 'msg': 'success'}

# select_rooms(token, "omb_2cbd7aac59a2292a577547e6d5ef6300")
# 会议室列表信息返回结果： {'code': 0, 'data': {'has_more': False, 'rooms': [{'building_id': 'omb_2cbd7aac59a2292a577547e6d5ef6300', 'building_name': '万通中心D座', 'capacity': 10, 'description': '', 'display_id': 'FM270155318', 'floor_name': 'F25', 'is_disabled': True, 'name': '25层休息室', 'room_id': 'omm_5678d2e7eab76c137ffd1e0f4c5deb8d'}, {'building_id': 'omb_2cbd7aac59a2292a577547e6d5ef6300', 'building_name': '万通中心D座', 'capacity': 12, 'description': '', 'display_id': 'FM847578908', 'floor_name': 'F10', 'is_disabled': False, 'name': 'Hacker', 'room_id': 'omm_fce8075d5a6a25c764a808c69a48b82a'}, {'building_id': 'omb_2cbd7aac59a2292a577547e6d5ef6300', 'building_name': '万通中心D座', 'capacity': 8, 'description': '', 'display_id': 'FM806540044', 'floor_name': 'F25', 'is_disabled': False, 'name': 'smart', 'room_id': 'omm_435bca3a3d40f120c63540028b965538'}, {'building_id': 'omb_2cbd7aac59a2292a577547e6d5ef6300', 'building_name': '万通中心D座', 'capacity': 10, 'description': '', 'display_id': 'FM673744413', 'floor_name': 'F25', 'is_disabled': False, 'name': 'think different', 'room_id': 'omm_d511e9e4e40f68107f556c943ca50c44'}, {'building_id': 'omb_2cbd7aac59a2292a577547e6d5ef6300', 'building_name': '万通中心D座', 'capacity': 90, 'description': '', 'display_id': 'FM571166897', 'floor_name': 'F23', 'is_disabled': False, 'name': '分享', 'room_id': 'omm_2fa172ec56aba79c654ec5a4b58e9f27'}, {'building_id': 'omb_2cbd7aac59a2292a577547e6d5ef6300', 'building_name': '万通中心D座', 'capacity': 12, 'description': '', 'display_id': 'FM384064710', 'floor_name': 'F10', 'is_disabled': False, 'name': '北极星', 'room_id': 'omm_3864b3539c370d51e8d086791b008d44'}, {'building_id': 'omb_2cbd7aac59a2292a577547e6d5ef6300', 'building_name': '万通中心D座', 'capacity': 8, 'description': '', 'display_id': 'FM122551240', 'floor_name': 'F10', 'is_disabled': False, 'name': '坦诚', 'room_id': 'omm_247693a0dbb368b6af624c51ba5df218'}, {'building_id': 'omb_2cbd7aac59a2292a577547e6d5ef6300', 'building_name': '万通中心D座', 'capacity': 4, 'description': '', 'display_id': 'FM428664952', 'floor_name': 'F10', 'is_disabled': False, 'name': '天权星', 'room_id': 'omm_32be015ee6d9318e11561b984d665971'}, {'building_id': 'omb_2cbd7aac59a2292a577547e6d5ef6300', 'building_name': '万通中心D座', 'capacity': 5, 'description': '', 'display_id': 'FM203632598', 'floor_name': 'F10', 'is_disabled': False, 'name': '天枢星', 'room_id': 'omm_dcf65c2ffcbabe4bf01c72e0470c541b'}, {'building_id': 'omb_2cbd7aac59a2292a577547e6d5ef6300', 'building_name': '万通中心D座', 'capacity': 7, 'description': '', 'display_id': 'FM388930916', 'floor_name': 'F10', 'is_disabled': False, 'name': '天狼星', 'room_id': 'omm_7e99a24f850323e3038526ce3f809ba5'}, {'building_id': 'omb_2cbd7aac59a2292a577547e6d5ef6300', 'building_name': '万通中心D座', 'capacity': 4, 'description': '', 'display_id': 'FM822301525', 'floor_name': 'F10', 'is_disabled': False, 'name': '天玑星', 'room_id': 'omm_fecbfd6505548d491026365ad03cb215'}, {'building_id': 'omb_2cbd7aac59a2292a577547e6d5ef6300', 'building_name': '万通中心D座', 'capacity': 5, 'description': '', 'display_id': 'FM412739092', 'floor_name': 'F10', 'is_disabled': False, 'name': '天璇星', 'room_id': 'omm_ddee0861011df191f0404b80f0c7d9eb'}, {'building_id': 'omb_2cbd7aac59a2292a577547e6d5ef6300', 'building_name': '万通中心D座', 'capacity': 5, 'description': '', 'display_id': 'FM223308813', 'floor_name': 'F10', 'is_disabled': False, 'name': '天衡星', 'room_id': 'omm_e457d7a3eb7133f98fc27a267a1646c1'}, {'building_id': 'omb_2cbd7aac59a2292a577547e6d5ef6300', 'building_name': '万通中心D座', 'capacity': 10, 'description': '', 'display_id': 'FM736325410', 'floor_name': 'F23', 'is_disabled': False, 'name': '太阳', 'room_id': 'omm_d47dd4f223a3531f31b351513b036f61'}, {'building_id': 'omb_2cbd7aac59a2292a577547e6d5ef6300', 'building_name': '万通中心D座', 'capacity': 31, 'description': '', 'display_id': 'FM324408629', 'floor_name': 'F23', 'is_disabled': False, 'name': '尽责', 'room_id': 'omm_41510695cc2c9e86c3ef7d4afc247c74'}, {'building_id': 'omb_2cbd7aac59a2292a577547e6d5ef6300', 'building_name': '万通中心D座', 'capacity': 6, 'description': '', 'display_id': 'FM812976651', 'floor_name': 'F23', 'is_disabled': False, 'name': '开放', 'room_id': 'omm_9da759bfae9935249eda2ce675e2682e'}, {'building_id': 'omb_2cbd7aac59a2292a577547e6d5ef6300', 'building_name': '万通中心D座', 'capacity': 6, 'description': '', 'display_id': 'FM195499232', 'floor_name': 'F10', 'is_disabled': False, 'name': '开阳星', 'room_id': 'omm_56bb92f696093b60a3108ae3b7102a78'}, {'building_id': 'omb_2cbd7aac59a2292a577547e6d5ef6300', 'building_name': '万通中心D座', 'capacity': 6, 'description': '', 'display_id': 'FM927896315', 'floor_name': 'F10', 'is_disabled': False, 'name': '摇光星', 'room_id': 'omm_2db12593ce9242345be73a59a0120ccc'}, {'building_id': 'omb_2cbd7aac59a2292a577547e6d5ef6300', 'building_name': '万通中心D座', 'capacity': 7, 'description': '', 'display_id': 'FM816184307', 'floor_name': 'F25', 'is_disabled': False, 'name': '敢干', 'room_id': 'omm_4a260a86bc05a2d7dbb901c53bf5bc92'}, {'building_id': 'omb_2cbd7aac59a2292a577547e6d5ef6300', 'building_name': '万通中心D座', 'capacity': 5, 'description': '', 'display_id': 'FM928457316', 'floor_name': 'F10', 'is_disabled': False, 'name': '敢想', 'room_id': 'omm_001832945aef034f5853ca649db51b97'}, {'building_id': 'omb_2cbd7aac59a2292a577547e6d5ef6300', 'building_name': '万通中心D座', 'capacity': 15, 'description': '', 'display_id': 'FM534527655', 'floor_name': 'F10', 'is_disabled': False, 'name': '敢说', 'room_id': 'omm_5a1d13dc13e79e6f739b3d6f2d26c452'}, {'building_id': 'omb_2cbd7aac59a2292a577547e6d5ef6300', 'building_name': '万通中心D座', 'capacity': 10, 'description': '', 'display_id': 'FM593467653', 'floor_name': 'F25', 'is_disabled': False, 'name': '敢败', 'room_id': 'omm_1898ce77b933009c84cc999a93aeefc4'}, {'building_id': 'omb_2cbd7aac59a2292a577547e6d5ef6300', 'building_name': '万通中心D座', 'capacity': 8, 'description': '', 'display_id': 'FM184513693', 'floor_name': 'F25', 'is_disabled': False, 'name': '极致', 'room_id': 'omm_a77aef5161de2d637bc0c156647474d4'}, {'building_id': 'omb_2cbd7aac59a2292a577547e6d5ef6300', 'building_name': '万通中心D座', 'capacity': 4, 'description': '', 'display_id': 'FM515576401', 'floor_name': 'F10', 'is_disabled': False, 'name': '泰山', 'room_id': 'omm_bb38d0046d5159a31385030a1346a6c5'}, {'building_id': 'omb_2cbd7aac59a2292a577547e6d5ef6300', 'building_name': '万通中心D座', 'capacity': 12, 'description': '', 'display_id': 'FM288439159', 'floor_name': 'F10', 'is_disabled': False, 'name': '浪漫', 'room_id': 'omm_a5ec3a14a94322968cd6fea05b34f4df'}, {'building_id': 'omb_2cbd7aac59a2292a577547e6d5ef6300', 'building_name': '万通中心D座', 'capacity': 6, 'description': '', 'display_id': 'FM566583597', 'floor_name': 'F23', 'is_disabled': False, 'name': '禾口', 'room_id': 'omm_e8f296a80f0f448a9d6c659abb0a7ea8'}, {'building_id': 'omb_2cbd7aac59a2292a577547e6d5ef6300', 'building_name': '万通中心D座', 'capacity': 6, 'description': '', 'display_id': 'FM209870318', 'floor_name': 'F23', 'is_disabled': False, 'name': '蓝点', 'room_id': 'omm_c520c17858b4b6fb22bac99f6e1dda5b'}, {'building_id': 'omb_2cbd7aac59a2292a577547e6d5ef6300', 'building_name': '万通中心D座', 'capacity': 6, 'description': '', 'display_id': 'FM414977638', 'floor_name': 'F25', 'is_disabled': True, 'name': '财务室', 'room_id': 'omm_0768126ff7d7da083bbb3f2e3637dcfa'}, {'building_id': 'omb_2cbd7aac59a2292a577547e6d5ef6300', 'building_name': '万通中心D座', 'capacity': 5, 'description': '', 'display_id': 'FM576257230', 'floor_name': 'F10', 'is_disabled': False, 'name': '超越', 'room_id': 'omm_9ca36d25bfe178df5da26205b39da278'}]}, 'msg': 'success'}

# user = select_userinfo(token, "liangliang.yan@yeepay.com")
# 用户信息返回结果： {'code': 0, 'data': {'user_list': [{'email': 'liangliang.yan@yeepay.com', 'status': {'is_activated': True, 'is_exited': False, 'is_frozen': False, 'is_resigned': False, 'is_unjoin': False}, 'user_id': 'ou_1a32c82be0a5c6ee7bc8debd75c65e34'}]}, 'msg': 'success'}

calendar_id = create_calendar_id(token)

grant_calendar(token, calendar_id, "writer", "ou_1a32c82be0a5c6ee7bc8debd75c65e34")

calendar = create_calendar(token, calendar_id, {
    "summary": "严亮亮日程标题",
    "description": "严亮亮日程描述",
    "need_notification": "false",
    "start_time": {
        "timestamp": "1712008800",
        "timezone": "Asia/Shanghai"
    },
    "end_time": {
        "timestamp": "1712016000",
        "timezone": "Asia/Shanghai"
    },
    "vchat": {
        "vc_type": "no_meeting",
        "icon_type": "default",
        "description": "",
        "meeting_url": "https://example.com",
        "meeting_settings": {

        }
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

# omm_4a260a86bc05a2d7dbb901c53bf5bc92 敢干
# omm_1898ce77b933009c84cc999a93aeefc4 敢败
add_calendar_user(token, calendar_id, event_id, {
    "attendees": [
        {
            "type": "user",
            "is_optional": "true",
            "user_id": "ou_1a32c82be0a5c6ee7bc8debd75c65e34",
            "room_id": "omm_1898ce77b933009c84cc999a93aeefc4"
        }
    ],
    "need_notification": "false",
    "is_enable_admin": "false",
    "add_operator_to_attendee": "true"
})
add_calendar_room(token, calendar_id, event_id, {
    "attendees": [
        {
            "type": "resource",
            "room_id": "omm_1898ce77b933009c84cc999a93aeefc4"
        }
    ],
    "need_notification": "false",
    "is_enable_admin": "false",
    "add_operator_to_attendee": "true"
})

select_room_free_busy(token, ["omm_4a260a86bc05a2d7dbb901c53bf5bc92", "omm_1898ce77b933009c84cc999a93aeefc4"],
                      "2024-04-02T06:00:00+08:00", "2024-04-02T10:00:00+08:00")
