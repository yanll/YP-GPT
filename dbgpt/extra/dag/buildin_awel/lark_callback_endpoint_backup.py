import json
import logging
import os
from typing import Dict

from langchain_openai import AzureChatOpenAI

from dbgpt.core.awel import DAG, HttpTrigger, MapOperator
from dbgpt.util.azure_util import create_azure_llm
from datetime import datetime
from dbgpt.util import larkutil


class RequestHandleOperator(MapOperator[Dict, str]):
    llm = None

    def __init__(self, **kwargs):
        self.llm = create_azure_llm()
        super().__init__(**kwargs)

    async def map(self, input_body: Dict) -> str:
        try:
            print(f"Receive input body: {input_body}")
            # 首次验证挑战码
            if "challenge" in input_body:
                return {"challenge": input_body["challenge"]}
            form_value = input_body['event']['action']['form_value']
            room_id = ""
            room_name = form_value['room']
            date = form_value['date'].replace("+0800", "")
            start_time = date + form_value['start']
            end_time = date + form_value['end']
            if room_name == "敢干":
                room_id = "omm_4a260a86bc05a2d7dbb901c53bf5bc92"
            if room_name == "极致":
                room_id = "omm_a77aef5161de2d637bc0c156647474d4"
            result = create_calendar(
                title="我的测试日程",
                name=room_name,
                room_id=room_id,
                start_time=start_time,
                end_time=end_time
            )

            return {
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
                        "template_id": "AAqkwmwOTohjy", "template_version_name": "1.0.10",
                        "template_variable": {
                            "ai_message": "请提供完整的信息！"
                        }
                    }
                }
            }
        except Exception as e:
            logging.exception("飞书回调处理异常！", e)
            return {"message": "OK"}


with DAG("dbgpt_awel_lark_callback_endpoint") as dag:
    trigger = HttpTrigger(
        endpoint="/lark_callback_endpoint",
        methods="POST",
        request_body=Dict
    )
    map_node = RequestHandleOperator()
    trigger >> map_node


def create_calendar(title, name, room_id, start_time, end_time):
    # omm_4a260a86bc05a2d7dbb901c53bf5bc92 敢干
    # omm_1898ce77b933009c84cc999a93aeefc4 敢败
    print("开始创建日程：", name, room_id, start_time, end_time)
    grant_user_open_id = "ou_1a32c82be0a5c6ee7bc8debd75c65e34"
    summary = title
    description = title
    s_time = int(datetime.strptime(start_time, "%Y-%m-%d %H:%M").timestamp())
    e_time = int(datetime.strptime(end_time, "%Y-%m-%d %H:%M").timestamp())

    token = larkutil.get_tenant_access_token()['tenant_access_token']
    calendar_id = larkutil.create_calendar_id(token=token)
    larkutil.grant_calendar(token, calendar_id, "writer", grant_user_open_id)

    calendar = larkutil.create_calendar(token, calendar_id, {
        "summary": summary,
        "description": description,
        "need_notification": "false",
        "start_time": {
            "timestamp": str(s_time),
            "timezone": "Asia/Shanghai"
        },
        "end_time": {
            "timestamp": str(e_time),
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
    print("已经创建的日历：", calendar)
    event_id = calendar['data']['event']['event_id']

    larkutil.add_calendar_user(token, calendar_id, event_id, {
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
    if (room_id):
        print("开始尝试预定会议室：", name, room_id)
        larkutil.add_calendar_room(token, calendar_id, event_id, {
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
    return '预定成功！'
