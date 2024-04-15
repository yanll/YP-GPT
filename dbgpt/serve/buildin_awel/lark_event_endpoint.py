import json
from typing import Dict
import os
import logging
from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate

from dbgpt.core.awel import DAG, HttpTrigger, MapOperator
from dbgpt.util import larkutil
from langchain_openai import AzureChatOpenAI
import asyncio


class RequestHandleOperator(MapOperator[Dict, str]):
    llm = None

    def __init__(self, **kwargs):
        os.environ["OPENAI_API_VERSION"] = os.getenv("PROXY_API_VERSION")
        os.environ["AZURE_OPENAI_ENDPOINT"] = os.getenv("AZURE_OPENAI_ENDPOINT")
        os.environ["AZURE_OPENAI_API_KEY"] = os.getenv("AZURE_OPENAI_KEY")

        self.llm = AzureChatOpenAI(
            deployment_name=os.getenv("API_AZURE_DEPLOYMENT")
        )
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
                asyncio.create_task(handle(self.llm, sender_open_id, content_text))
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


async def handle(llm, sender_open_id, human_message):
    print("lark_event_endpoint async handle：", human_message)
    prompt = PromptTemplate(
        template="{msg}",
        input_variables=["msg"]
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    ai_message = chain.invoke({"msg": human_message})
    content = {"text": human_message + "：\n\n" + ai_message["text"]}
    larkutil.send_message(
        receive_id=sender_open_id,
        content=content,
        receive_id_type="open_id"
    )
