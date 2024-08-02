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
from dbgpt.storage.chat_history import ChatHistoryMessageEntity
from dbgpt.storage.chat_history.chat_history_db import ChatHistoryMessageDao
from dbgpt.extra.dag.buildin_awel.langgraph.nl2sql.nl2sql_assistant import Nl2sqlAssistant
from dbgpt.util import nl2sql_util


class RequestHandleOperator(MapOperator[Dict, str]):

    def __init__(self, **kwargs):
        self.chat_history_message_dao = ChatHistoryMessageDao()
        self.gpts_app_service = GptsAppService()
        self.app_chat_service = AppChatService()
        self.nl2sql_assistant = Nl2sqlAssistant()
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
            event_id = headers["event_id"]
            if (event_type not in ["im.message.receive_v1",
                                   "p2p_chat_create",
                                   "im.chat.member.bot.added_v1",
                                   "im.chat.member.bot.deleted_v1"
                                   ]):
                return {"message": "OK"}

            redis_key = "nl2sql_event_id_for_no_repeat_" + event_id

            exists: str = self.redis_client.get(redis_key)
            if (exists == "true"):
                print("飞书事件已经存在，跳过执行：", input_body)
                return {"message": "OK"}
            else:
                self.redis_client.set(redis_key, "true", 12 * 60 * 60)

            event = input_body["event"]

            if (event_type == "p2p_chat_create"):
                print("机器人会话被创建", event)
                return {"message": "OK"}
            if (event_type == "im.chat.member.bot.added_v1"):
                print("机器人进群了", event)
                return {"message": "OK"}
            if (event_type == "im.chat.member.bot.deleted_v1"):
                print("机器人被群踢了", event)
                return {"message": "OK"}

            sender_open_id = event["sender"]["sender_id"]["open_id"]
            message = event["message"]
            message_type = message["message_type"]
            chat_type = message["chat_type"]
            content = json.loads(message["content"])
            content_text = content["text"]
            # apps = self.gpts_app_service.get_gpts_app_list("singe_agent")
            # print("应用列表：", apps)
            if event_type == "im.message.receive_v1" and message_type == "text" and sender_open_id != "" and content_text != "" and chat_type == "p2p":
                print("开始异步执行", event_id)
                asyncio.create_task(
                    request_handle(self.app_chat_service, self.nl2sql_assistant, sender_open_id, content_text)
                )
                print("执行日志", event_id)
            return {"message": "OK"}
        except Exception as e:
            logging.exception("飞书事件处理异常！", e)
            return {"message": "OK"}


with DAG("dbgpt_awel_nl2sql_endpoint") as dag:
    trigger = HttpTrigger(
        endpoint="/nl2sql_endpoint",
        methods="POST",
        request_body=Dict
    )

    map_node = RequestHandleOperator()
    trigger >> map_node


async def request_handle(app_chat_service: AppChatService, nl2sql_assistant: Nl2sqlAssistant, sender_open_id,
                         human_message):
    print("nl2sql_endpoint async handle：", human_message)

    # 开启新会话，归档历史消息。
    if (human_message == "new chat"):
        app_chat_service.disable_app_chat_his_message_by_uid(sender_open_id)
        return None

    try:
        # 获取调用模型获取的信息
        rs = await nl2sql_assistant.handle(human_message, sender_open_id)


        resp_msg = str(rs)
        if (isinstance(rs, Dict)):
            agent_outcome = rs['agent_outcome']
            if (isinstance(agent_outcome, AgentFinish)):
                resp_msg = agent_outcome.return_values['output']
        # 返回消息
        nl2sql_util.send_message(
            human_message=human_message,
            receive_id=sender_open_id,
            content={"text": resp_msg},
            receive_id_type="open_id"
        )
        print("Nl2sqlResult:", resp_msg)
    except Exception as e:
        logging.error("数据分析助手运行异常：", e)
        raise e


