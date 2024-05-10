import logging
from typing import List, Dict

from dbgpt.extra.dag.buildin_awel.app.app_chat_db import AppChatDao
from dbgpt.extra.dag.buildin_awel.app.gpts_app_db import GptsAppDao

logger = logging.getLogger(__name__)


class GptsAppService:
    def __init__(self):
        self.gpts_app_dao = GptsAppDao()

    def get_gpts_app_list(self, team_mode: str = None) -> List:
        list = self.gpts_app_dao.get_gpts_app_list(team_mode)
        rs = []
        for row in list:
            rs.append({
                "app_code": row["app_code"],
                "app_name": row["app_describe"]
            })
        return rs


class AppChatService:
    def __init__(self):
        self.app_chat_dao = AppChatDao()

    def add_app_chat_his_message(self, rec: Dict) -> int:
        return self.app_chat_dao.add_app_chat_his_message(rec)

    def disable_app_chat_his_message_by_uid(self, conv_uid: str) -> int:
        return self.app_chat_dao.disable_app_chat_his_message_by_uid(conv_uid)

    async def a_disable_app_chat_his_message_by_uid(self, conv_uid: str) -> int:
        return self.app_chat_dao.disable_app_chat_his_message_by_uid(conv_uid)

    def a_update_app_chat_his_message_like_by_uid_mid(self, comment: str, conv_uid: str, message_id: str) -> int:
        return self.app_chat_dao.a_update_app_chat_his_message_like_by_uid_mid(comment, conv_uid, message_id)

    def get_app_chat_his_messages_by_conv_uid(self, conv_uid, status: str = "ENABLED") -> List:
        list = self.app_chat_dao.get_app_chat_his_messages_by_conv_uid(conv_uid, status)
        rs = []
        for row in list:
            rs.append({
                "role": row["message_type"],
                "content": row["content"]
            })
        return rs
