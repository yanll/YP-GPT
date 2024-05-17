from typing import Dict, List

from sqlalchemy import text

from dbgpt.storage.metadata import BaseDao
from dbgpt.util.lark import larkutil
import logging


class AppChatDao(BaseDao):

    def add_app_chat_his_message(self, rec: Dict) -> int:
        rec['nickname'] = ''
        rec['en_name'] = ''
        rec['union_id'] = ''
        try:
            userinfo = larkutil.select_userinfo(open_id=rec['conv_uid'])
            if userinfo:
                if "name" in userinfo:
                    rec['nickname'] = userinfo["name"]
                if 'en_name' in userinfo:
                    rec['en_name'] = userinfo["en_name"]
                if 'union_id' in userinfo:
                    rec['union_id'] = userinfo["union_id"]
        except Exception as e:
            logging.warning("用户姓名解析异常")
        session = self.get_raw_session()
        statement = text(
            """
            insert into app_chat_history_message(id, agent_name, conv_uid, message_type, content, message_detail, display_type, lark_message_id, nickname, en_name, union_id) values (:id, :agent_name, :conv_uid, :message_type, :content, :message_detail, :display_type, :lark_message_id, :nickname, :en_name, :union_id)
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

    def a_update_app_chat_his_message_like_by_uid_mid(self, comment_type: str, conv_uid: str, message_id: str) -> int:
        if comment_type == "" and conv_uid == "" and message_id == "":
            return 0
        session = self.get_raw_session()
        statement = text(
            """
            update app_chat_history_message set comment_type = :comment_type where conv_uid = :conv_uid and lark_message_id = :lark_message_id
            """
        )
        session.execute(
            statement, {
                "comment_type": comment_type,
                "conv_uid": conv_uid,
                "lark_message_id": message_id
            }
        )
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

    def add_app_feedback(self, rec: Dict) -> int:
        rec['nickname'] = ''
        rec['en_name'] = ''
        rec['union_id'] = ''
        try:
            userinfo = larkutil.select_userinfo(open_id=rec['conv_uid'])
            if userinfo:
                if "name" in userinfo:
                    rec['nickname'] = userinfo["name"]
                if 'en_name' in userinfo:
                    rec['en_name'] = userinfo["en_name"]
                if 'union_id' in userinfo:
                    rec['union_id'] = userinfo["union_id"]
        except Exception as e:
            logging.warning("用户姓名解析异常")
        session = self.get_raw_session()
        statement = text(
            """
            insert into app_feedback(id, scope, conv_uid, lark_message_id, feedback, recommendation, effect, reference_url, nickname, en_name, union_id) values (:id, :scope, :conv_uid, :lark_message_id, :feedback, :recommendation, :effect, :reference_url, :nickname, :en_name, :union_id)
            """
        )
        session.execute(statement, rec)
        session.commit()
        session.close()
        return 0
