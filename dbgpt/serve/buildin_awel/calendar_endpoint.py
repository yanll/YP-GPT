import json
from typing import Dict, List
import os
import logging
from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate

from dbgpt.core import SystemPromptTemplate, MessagesPlaceholder, HumanPromptTemplate, InMemoryStorage
from dbgpt.core.awel import DAG, HttpTrigger, MapOperator
from dbgpt.core.interface.operators.composer_operator import ChatHistoryPromptComposerOperator
from dbgpt.core.schema.api import ChatCompletionResponse
from dbgpt.storage.chat_history import ChatHistoryMessageEntity
from dbgpt.storage.chat_history.chat_history_db import ChatHistoryMessageDao
from dbgpt.util import larkutil
from langchain_openai import AzureChatOpenAI
import asyncio
from dbgpt.util.azure_util import create_azure_llm
from langchain_core.messages import HumanMessage
from langgraph.graph import END, MessageGraph
from dbgpt.client import Client


class RequestHandleOperator(MapOperator[Dict, str]):
    llm = None

    def __init__(self, **kwargs):
        self.chat_history_message_dao = ChatHistoryMessageDao()
        self.llm = create_azure_llm()
        super().__init__(**kwargs)

    async def map(self, input_body: Dict) -> str:
        try:
            print(f"Receive input body: {input_body}")
            # 首次验证挑战码
            if "challenge" in input_body:
                return {"challenge": input_body["challenge"]}

            header = input_body["header"]
            event = input_body["event"]
            sender_open_id = event["sender"]["sender_id"]["open_id"]
            message = event["message"]
            message_type = message["message_type"]
            chat_type = message["chat_type"]
            content = json.loads(message["content"])
            content_text = content["text"]

            if message_type == "text" and sender_open_id != "" and content_text != "" and chat_type == "p2p":
                asyncio.create_task(handle(self.llm, self.chat_history_message_dao, sender_open_id, content_text))
            return {"message": "OK"}
        except Exception as e:
            logging.exception("飞书事件处理异常！", e)
            return {"message": "OK"}


with DAG("dbgpt_awel_calendar_endpoint") as dag:
    trigger = HttpTrigger(
        endpoint="/calendar_endpoint",
        methods="POST",
        request_body=Dict
    )

    map_node = RequestHandleOperator()
    trigger >> map_node


async def handle(llm, chat_history_dao: ChatHistoryMessageDao, sender_open_id, human_message):
    print("calendar_endpoint async handle：", human_message)

    graph = MessageGraph()
    graph.add_node("extract_goal", call_extract_goal)
    graph.add_edge("extract_goal", END)
    graph.set_entry_point("extract_goal")
    runnable = graph.compile()
    messages = []
    his: List[ChatHistoryMessageEntity] = chat_history_dao.get_his_messages_by_uid(sender_open_id)
    his: List[ChatHistoryMessageEntity] = []
    if his:
        for m in his:
            dict = json.loads(m.message_detail)
            if dict["type"] == "human":
                messages.append(HumanMessage(name=sender_open_id, content="human:" + dict["data"]["content"]))
            if dict["type"] == "ai":
                messages.append(HumanMessage(name=sender_open_id, content="ai:" + dict["data"]["content"]))
    messages.append(HumanMessage(name=sender_open_id, content="human:" + human_message))
    await runnable.ainvoke(messages)


async def call_extract_goal(messages: List[HumanMessage]):
    DBGPT_API_KEY = "dbgpt"
    client = Client(api_key=DBGPT_API_KEY)
    mess = [
        "你是一个内容专家，请从用户和AI的对话信息中识别出用户的意图，当用户的意图是'会议室预定'或'创建日程'时，回复：'MEETING_ROOM_BINGO'，否则按照正常的AI助手回复。\n"
        "以下是用户和AI的对话内容：\n"
        "\n\n"
    ]
    conv_uid = messages[0].name
    for m in messages:
        mess.append(m.content + "\n")
    res: ChatCompletionResponse = await client.chat(
        model="proxyllm",
        messages="".join(mess),
        conv_uid=conv_uid
    )
    ai_message = res.choices[0].message.content
    print("执行结果：", ai_message)
    if (ai_message != "MEETING_ROOM_BINGO"):
        larkutil.send_message(
            receive_id=conv_uid,
            content={"text": ai_message.replace("AI: ", "")},
            receive_id_type="open_id"
        )
    else:
        larkutil.send_message(
            receive_id="ou_1a32c82be0a5c6ee7bc8debd75c65e34",
            content={
                "type": "template",
                "data": {
                    "template_id": "AAqkwmwOTohjy", "template_version_name": "1.0.10",
                    "template_variable": {
                        "ai_message": "请提供完整的信息！"
                    }
                }
            },
            receive_id_type="open_id",
            msg_type="interactive"
        )
    return res



