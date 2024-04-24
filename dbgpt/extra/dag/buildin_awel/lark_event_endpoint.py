import asyncio
import json
import logging
import re
from typing import Dict, List

from langchain_core.agents import AgentFinish

from dbgpt.client import Client
from dbgpt.core.awel import DAG, HttpTrigger, MapOperator
from dbgpt.extra.cache.redis_cli import RedisClient
from dbgpt.extra.dag.buildin_awel.app.service import GptsAppService, AppChatService
from dbgpt.extra.dag.buildin_awel.langgraph.assistants.sales_assistant import SalesAssistant
from dbgpt.extra.dag.buildin_awel.lark import lark_event_handler
from dbgpt.storage.chat_history import ChatHistoryMessageEntity
from dbgpt.storage.chat_history.chat_history_db import ChatHistoryMessageDao
from dbgpt.util import larkutil


class RequestHandleOperator(MapOperator[Dict, str]):

    def __init__(self, **kwargs):
        self.chat_history_message_dao = ChatHistoryMessageDao()
        self.gpts_app_service = GptsAppService()
        self.app_chat_service = AppChatService()
        self.sales_assistant = SalesAssistant()
        self.redis_client = RedisClient()
        super().__init__(**kwargs)

    async def map(self, input_body: Dict) -> Dict:
        try:
            print(f"接收飞书事件: {input_body}")
            # 首次验证挑战码
            if "challenge" in input_body:
                return {"challenge": input_body["challenge"]}
            headers = input_body["header"]
            event_type = headers["event_type"]
            event_id = headers["event_type"]
            if lark_event_handler.valid_event_type(input_body) is False:
                return {}
            if lark_event_handler.valid_repeat(self.redis_client, input_body) is False:
                return {}

            event = input_body["event"]

            # apps = self.gpts_app_service.get_gpts_app_list("singe_agent")
            # print("应用列表：", apps)
            if event_type == "im.message.receive_v1":
                sender_open_id = event["sender"]["sender_id"]["open_id"]
                message = event["message"]
                message_type = message["message_type"]
                chat_type = message["chat_type"]
                content = json.loads(message["content"])
                content_text = content["text"]
                if (message_type == "text" and content_text != "" and chat_type == "p2p" and sender_open_id != ""):
                    print("开始异步执行", event_id)
                    asyncio.create_task(
                        request_handle(self.app_chat_service, self.sales_assistant, sender_open_id, content_text)
                    )
                    print("执行日志", event_id)
            return {"message": "OK"}
        except Exception as e:
            logging.exception("飞书事件处理异常！", e)
            return {"message": "OK"}


with DAG("dbgpt_awel_lark_event_endpoint") as dag:
    trigger = HttpTrigger(
        endpoint="/lark_event_endpoint",
        methods="POST",
        request_body=Dict
    )

    map_node = RequestHandleOperator()
    trigger >> map_node


async def request_handle(app_chat_service: AppChatService, sales_assistant: SalesAssistant, sender_open_id,
                         human_message):
    print("lark_event_endpoint async handle：", human_message)

    # 开启新会话，归档历史消息。
    if (human_message == "new chat"):
        app_chat_service.disable_app_chat_his_message_by_uid(sender_open_id)
        return None

    rs = sales_assistant._run(input=human_message, conv_uid=sender_open_id)
    resp_msg = str(rs)
    if (isinstance(rs, Dict)):
        agent_outcome = rs['agent_outcome']
        if (isinstance(agent_outcome, AgentFinish)):
            resp_msg = agent_outcome.return_values['output']
    larkutil.send_message(
        receive_id=sender_open_id,
        content={"text": resp_msg},
        receive_id_type="open_id"
    )
    print("LarkEventHandleResult:", resp_msg)
