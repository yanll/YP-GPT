import json
from typing import Dict

from langchain_core.agents import AgentFinish

from dbgpt.extra.cache.redis_cli import RedisClient
from dbgpt.extra.dag.buildin_awel.app.service import GptsAppService, AppChatService
from dbgpt.extra.dag.buildin_awel.langgraph.assistants.sales_assistant import SalesAssistant
from dbgpt.storage.chat_history.chat_history_db import ChatHistoryMessageDao
from dbgpt.util import larkutil


class LarkEventHandler:

    def __init__(self, **kwargs):
        self.chat_history_message_dao = ChatHistoryMessageDao()
        self.gpts_app_service = GptsAppService()
        self.app_chat_service = AppChatService()
        self.sales_assistant = SalesAssistant()
        self.redis_client = RedisClient()
        super().__init__(**kwargs)

    def valid_event_type(self, input_body: Dict) -> bool:
        headers = input_body["header"]
        event_type = headers["event_type"]

        if event_type == "p2p_chat_create":
            print("机器人会话被创建", input_body)
        if event_type == "im.chat.member.bot.added_v1":
            print("机器人进群了", input_body)
        if event_type == "im.chat.member.bot.deleted_v1":
            print("机器人被群踢了", input_body)

        event_types = [
            "im.message.receive_v1", "p2p_chat_create", "im.chat.member.bot.added_v1", "im.chat.member.bot.deleted_v1"
        ]
        if event_type in event_types:
            return True
        return False

    def valid_repeat(self, input_body: Dict) -> bool:
        headers = input_body["header"]
        event_id = headers["event_id"]
        redis_key = "lark_event_id_for_no_repeat_" + event_id
        exists: str = self.redis_client.get(redis_key)
        if exists == "true":
            print("飞书事件已经存在，跳过执行：", input_body)
            return False
        self.redis_client.set(redis_key, "true", 12 * 60 * 60)
        return True

    async def a_handle(self, input_body: Dict):
        print("LarkEventHandler_a_handle：", input_body)
        headers = input_body["header"]
        event_type = headers["event_type"]
        event_id = headers["event_id"]
        event = input_body["event"]
        if event_type == "im.message.receive_v1":
            sender_open_id = event["sender"]["sender_id"]["open_id"]
            message = event["message"]
            message_type = message["message_type"]
            chat_type = message["chat_type"]
            content = json.loads(message["content"])
            content_text = content["text"]
            if message_type == "text" and content_text != "" and chat_type == "p2p" and sender_open_id != "":
                self.handle_message(sender_open_id, content_text)
        else:
            pass

    def handle_message(self, sender_open_id, human_message):
        print("LarkEventHandler_handle_message:", human_message)
        # 开启新会话，归档历史消息。
        if human_message == "new chat":
            self.app_chat_service.disable_app_chat_his_message_by_uid(sender_open_id)
            return None

        rs = self.sales_assistant._run(input=human_message, conv_uid=sender_open_id)
        resp_msg = str(rs)
        if isinstance(rs, Dict):
            agent_outcome = rs['agent_outcome']
            if isinstance(agent_outcome, AgentFinish):
                resp_msg = agent_outcome.return_values['output']
        larkutil.send_message(
            receive_id=sender_open_id,
            content={"text": resp_msg},
            receive_id_type="open_id"
        )
        print("LarkEventHandler_handle_message_result:", resp_msg)
