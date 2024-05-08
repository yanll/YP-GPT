import json
import logging
from typing import Dict

import requests
from langchain_core.agents import AgentFinish

from dbgpt.extra.cache.redis_cli import RedisClient
from dbgpt.extra.dag.buildin_awel.app.service import GptsAppService, AppChatService
from dbgpt.extra.dag.buildin_awel.langgraph.assistants.sales_assistant import SalesAssistant
from dbgpt.storage.chat_history.chat_history_db import ChatHistoryMessageDao
from dbgpt.util import envutils
from dbgpt.util.lark import lark_card_util, ssoutil


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
        if event_type == "application.bot.menu_v6":
            print("触发自定义事件", input_body)

        event_types = [
            "im.message.receive_v1", "p2p_chat_create", "im.chat.member.bot.added_v1", "im.chat.member.bot.deleted_v1",
            "application.bot.menu_v6"
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
            self.new_chat(sender_open_id)
            return None

        rs = self.sales_assistant._run(input=human_message, conv_uid=sender_open_id)
        resp_msg = str(rs)
        last_output_dict = {}
        if isinstance(rs, Dict):
            agent_outcome = rs['agent_outcome']
            if isinstance(agent_outcome, AgentFinish):
                return_values = agent_outcome.return_values
                resp_msg = return_values['output']
                if "last_output" in return_values:
                    last_output = return_values["last_output"]
                    try:
                        if len(last_output) > 0:
                            last_output_dict = json.loads(last_output.replace("'", "\""))
                    except Exception as e:
                        logging.error("last_output_load_err：", last_output)
        print("LarkEventHandler_handle_message_result:", resp_msg)
        if last_output_dict and "display_type" in last_output_dict and last_output_dict["display_type"] == "form":
            print("已发送表单，跳过文本消息发送！")
            return
        lark_card_util.send_message_with_bingo(
            receive_id=sender_open_id,
            template_variable={
                "message_content": resp_msg
            }
        )

    def new_chat(self, sender_open_id):
        if True:
            url = envutils.getenv("FMC_ENDPOINT") + '/flowable/task/list'
            headers = {
                'yuiassotoken': ssoutil.get_sso_credential(open_id=sender_open_id),
                'Content-Type': 'application/json',
            }
            params = {
                "page": 1,
                "limit": 10
            }
            print(str(headers))
            resp = requests.request(method='GET', headers=headers, url=url, params=params)
            print("FMC返回结果：", resp.status_code)
        self.app_chat_service.disable_app_chat_his_message_by_uid(sender_open_id)
