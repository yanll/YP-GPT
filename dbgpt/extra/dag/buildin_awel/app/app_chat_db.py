from typing import Dict, List

from sqlalchemy import text

from dbgpt.storage.metadata import BaseDao


class AppChatDao(BaseDao):

    def add_app_chat_his_message(self, rec: Dict) -> int:
        session = self.get_raw_session()
        statement = text(
            """
            insert into app_chat_history_message(id, agent_name, conv_uid, message_type, content, message_detail) values (:id, :agent_name, :conv_uid, :message_type, :content, :message_detail)
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

    def get_app_chat_his_messages(self, status: str = "ENABLED") -> List:
        """最近30分钟的聊天记录"""
        session = self.get_raw_session()
        result = session.execute(
            statement=text(
                "SELECT * FROM app_chat_history_message where created_time >=DATE_SUB(NOW(), INTERVAL 30 MINUTE) and message_type in ('human', 'ai') and status = :status order by created_time asc"
            ),
            params={"status": status})
        rs = []
        for row in result:
            dic = row._asdict()
            rs.append(dic)
        return rs
