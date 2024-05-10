from typing import Dict, List

from sqlalchemy import text

from dbgpt.storage.metadata import BaseDao


class AppChatDao(BaseDao):

    def add_app_chat_his_message(self, rec: Dict) -> int:
        session = self.get_raw_session()
        statement = text(
            """
            insert into app_chat_history_message(id, agent_name, conv_uid, message_type, content, message_detail, display_type, lark_message_id) values (:id, :agent_name, :conv_uid, :message_type, :content, :message_detail, :display_type, :lark_message_id)
            """
        )
        session.execute(statement, rec)
        session.commit()
        session.close()
        return 0

    def disable_app_chat_his_message_by_uid(self, conv_uid: str) -> int:
        session = self.get_raw_session()
        statement = text(
            """
            update app_chat_history_message set status = 'DISABLED' where conv_uid = :conv_uid
            """
        )
        session.execute(statement, {"conv_uid": conv_uid})
        session.commit()
        session.close()
        return 0

    def get_app_chat_his_messages_by_conv_uid(self, conv_uid: str = "#", status: str = "ENABLED") -> List:
        """最近30分钟的聊天记录"""
        session = self.get_raw_session()
        result = session.execute(
            statement=text(
                "SELECT * FROM app_chat_history_message where conv_uid = :conv_uid and created_time >=DATE_SUB(NOW(), INTERVAL 30 MINUTE) and message_type in ('human', 'ai') and status = :status order by created_time asc"
            ),
            params={"conv_uid": conv_uid, "status": status})
        rs = []
        for row in result:
            dic = row._asdict()
            rs.append(dic)
        return rs
