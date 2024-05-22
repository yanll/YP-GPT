
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

