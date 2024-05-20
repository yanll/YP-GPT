import json
from typing import Dict

import requests

from dbgpt.extra.cache.redis_cli import RedisClient
from dbgpt.extra.dag.buildin_awel.app.service import AppChatService
from dbgpt.extra.dag.buildin_awel.langgraph.assistants.sales_assistant import SalesAssistant
from dbgpt.extra.dag.buildin_awel.langgraph.wrappers.lark_event_handler_wrapper import LarkEventHandlerWrapper
from dbgpt.util import envutils
from dbgpt.util.lark import ssoutil
from dbgpt.util.lark import lark_message_util


class LarkEventHandler:

    def __init__(self, **kwargs):
        self.app_chat_service = AppChatService()
        self.sales_assistant = SalesAssistant()
        self.lark_event_handler_wrapper = LarkEventHandlerWrapper()
        self.redis_client = RedisClient()
        super().__init__(**kwargs)

    def valid_event_type(self, input_body: Dict) -> bool:
        headers = input_body["header"]
        event_type = headers["event_type"]
        event_type2 = input_body['event'].get('type')

        if event_type == "p2p_chat_create" or event_type2 == "p2p_chat_create":
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

        if event_type2 in event_types:
            return True
        return False

    def valid_repeat(self, input_body: Dict) -> bool:

        # 首次进入会话校验，首次进入会话的event_id不能从heaer里拿
        if input_body["event"].get("type") == 'p2p_chat_create':
            event_id = input_body["uuid"]
            redis_key = "lark_event_id_for_no_repeat_" + event_id
            exists: str = self.redis_client.get(redis_key)
            if exists == "true":
                print("飞书事件已经存在，跳过执行：", input_body)
                return False
            self.redis_client.set(redis_key, "true", 12 * 60 * 60)
            return True

        # 其他对话情况的校验
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
                self.handle_human_message(sender_open_id, content_text)
        else:
            pass

    def handle_human_message(self, sender_open_id, human_message):
        print("LarkEventHandler_handle_message:", human_message)
        # 开启新会话，归档历史消息。
        if human_message == "new chat":
            self.new_chat(sender_open_id)
            return None

        # 发送loading卡片
        try:
            # comment: 
            message_id = lark_message_util.send_loading_message(receive_id=sender_open_id)
            assistant_response = self.sales_assistant._run(input=human_message, conv_uid=sender_open_id)
            self.lark_event_handler_wrapper.a_reply(sender_open_id, human_message, assistant_response)
            lark_message_util.update_loading_message(message_id=message_id, type="standard", content="小助理已为您处理完成！")
        except Exception as e:
            lark_message_util.update_loading_message(message_id=message_id, type="error", content="小助理不堪重任了！")
            raise e
        # end try

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
            print("FMC返回结果：<!DOCTYPE html", resp.text.startswith("<!DOCTYPE html"))
        self.app_chat_service.disable_app_chat_his_message_by_uid(sender_open_id)
