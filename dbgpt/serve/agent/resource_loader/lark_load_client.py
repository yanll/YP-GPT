import logging
from datetime import datetime
from typing import Optional

from dbgpt._private.config import Config
from dbgpt.agent.resource.resource_api import AgentResource
from dbgpt.agent.resource.resource_lark_api import ResourceLarkClient
from dbgpt.component import ComponentType
from dbgpt.util.executor_utils import ExecutorFactory
from dbgpt.util import larkutil

CFG = Config()

logger = logging.getLogger(__name__)


class LarkLoadClient(ResourceLarkClient):
    def __init__(self):
        super().__init__()
        # The executor to submit blocking function
        self._executor = CFG.SYSTEM_APP.get_component(
            ComponentType.EXECUTOR_DEFAULT, ExecutorFactory
        ).create()

    def get_data_type(self, resource: AgentResource) -> str:
        # conn = CFG.local_db_manager.get_connector(resource.value)
        # return conn.db_type
        return "lark"

    # 执行AI前调用
    async def a_get_userinfo(self, db: str, question: Optional[str] = None) -> str:
        userinfo = {"username": "管理员", "email": "adm@adm.com"}
        return userinfo

    # 获取AI结果后调用
    async def a_muti_table_add_record(self, app_id: str, table_id: str, record: dict) -> None:
        print("这里开始执行外部调用，Endpoint a_query！", record)
        return larkutil.muti_table_add_record(app_id=app_id, table_id=table_id, record=record)

    # 后置处理
    async def a_lark_after_notify(self, receive_id: str, text: str):
        content = {"text": text}
        return larkutil.send_message(receive_id, content)

    def get_meeting_room_status(self):
        if True:
            return ""
        token = larkutil.get_tenant_access_token()['tenant_access_token']
        sta = larkutil.select_room_free_busy(
            token=token,
            room_ids=["omm_fce8075d5a6a25c764a808c69a48b82a",
                      "omm_435bca3a3d40f120c63540028b965538",
                      "omm_d511e9e4e40f68107f556c943ca50c44",
                      "omm_2fa172ec56aba79c654ec5a4b58e9f27",
                      "omm_3864b3539c370d51e8d086791b008d44",
                      "omm_247693a0dbb368b6af624c51ba5df218",
                      "omm_32be015ee6d9318e11561b984d665971",
                      "omm_dcf65c2ffcbabe4bf01c72e0470c541b",
                      "omm_7e99a24f850323e3038526ce3f809ba5",
                      "omm_fecbfd6505548d491026365ad03cb215",
                      "omm_ddee0861011df191f0404b80f0c7d9eb",
                      "omm_e457d7a3eb7133f98fc27a267a1646c1",
                      "omm_d47dd4f223a3531f31b351513b036f61",
                      "omm_41510695cc2c9e86c3ef7d4afc247c74",
                      "omm_9da759bfae9935249eda2ce675e2682e",
                      "omm_56bb92f696093b60a3108ae3b7102a78",
                      "omm_2db12593ce9242345be73a59a0120ccc",
                      "omm_4a260a86bc05a2d7dbb901c53bf5bc92",
                      "omm_001832945aef034f5853ca649db51b97",
                      "omm_5a1d13dc13e79e6f739b3d6f2d26c452",
                      "omm_1898ce77b933009c84cc999a93aeefc4",
                      "omm_a77aef5161de2d637bc0c156647474d4",
                      "omm_bb38d0046d5159a31385030a1346a6c5",
                      "omm_a5ec3a14a94322968cd6fea05b34f4df",
                      "omm_e8f296a80f0f448a9d6c659abb0a7ea8",
                      "omm_c520c17858b4b6fb22bac99f6e1dda5b",
                      "omm_9ca36d25bfe178df5da26205b39da278"],
            time_min="2024-04-01T00:00:00+08:00",
            time_max="2024-04-10T00:00:00+08:00"
        )
        data = sta['data']['free_busy']
        return data

    async def create_calendar(self, title, name, room_id, start_time, end_time):
        # omm_4a260a86bc05a2d7dbb901c53bf5bc92 敢干
        # omm_1898ce77b933009c84cc999a93aeefc4 敢败
        print("开始创建日程：", name, room_id, start_time, end_time)
        grant_user_open_id = "ou_1a32c82be0a5c6ee7bc8debd75c65e34"
        summary = title
        description = title
        s_time = int(datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S").timestamp())
        e_time = int(datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S").timestamp())

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
