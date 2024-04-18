import asyncio
import json
import logging
from typing import Dict, List
import re

from langchain.chains.llm import LLMChain
from langchain_core.messages import HumanMessage
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, SystemMessagePromptTemplate, \
    HumanMessagePromptTemplate, MessagesPlaceholder
from langgraph.graph import END, MessageGraph

from dbgpt.client import Client
from dbgpt.core.awel import DAG, HttpTrigger, MapOperator
from dbgpt.core.schema.api import ChatCompletionResponse
from dbgpt.extra.cache.redis_cli import RedisClient
from dbgpt.extra.dag.buildin_awel.app.service import GptsAppService
from dbgpt.storage.chat_history import ChatHistoryMessageEntity
from dbgpt.storage.chat_history.chat_history_db import ChatHistoryMessageDao
from dbgpt.util import larkutil
from dbgpt.util.azure_util import create_azure_llm


class RequestHandleOperator(MapOperator[Dict, str]):
    llm = None

    def __init__(self, **kwargs):
        self.chat_history_message_dao = ChatHistoryMessageDao()
        self.gpts_app_service = GptsAppService()
        self.llm = create_azure_llm()
        super().__init__(**kwargs)

    async def map(self, input_body: Dict) -> str:
        try:
            print(f"接收飞书事件: {input_body}")
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
            apps = self.gpts_app_service.get_gpts_app_list("singe_agent")
            print("应用列表：", apps)
            if message_type == "text" and sender_open_id != "" and content_text != "" and chat_type == "p2p":
                await asyncio.create_task(request_handle(apps, self.llm, self.chat_history_message_dao, sender_open_id, content_text))
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


async def request_handle(apps, llm, chat_history_dao: ChatHistoryMessageDao, sender_open_id, human_message):
    print("lark_event_endpoint async handle：", human_message)

    his: List[ChatHistoryMessageEntity] = chat_history_dao.get_his_messages_by_uid(sender_open_id)
    # role_desc = (
    #     "你是一个内容专家，现在有以下应用：\n"
    #     f"{json.dumps(apps, ensure_ascii=False)}\n"
    #     "请根据我输入的内容识别我的意图，根据意图匹配需要使用哪个应用，如果意图匹配成功：按照{'app_code': 'the value of app_code', 'app_descpibe': 'the value of app_descpibe'}格式回复给我并且不要回复多余内容。\n"
    #     "如果识别不到我的意图：以普通AI助手的身份回答我的问题。"
    # )
    # "以下是我和AI的对话内容：\n"
    # "\n\n"

    # messages.append(HumanMessage(content="system:" + role_desc))
    # if his and len(his) > 0:
    #     for m in his:
    #         dict = json.loads(m.message_detail)
    #         if dict["type"] == "human":
    #             messages.append(HumanMessage(content="human:" + dict["data"]["content"]))
    #         if dict["type"] == "ai":
    #             messages.append(HumanMessage(content="ai:" + dict["data"]["content"]))
    await call_extract_app(llm, apps, sender_open_id, human_message, his)


async def call_extract_app(llm, apps, conv_uid, human_message: str, his: List):
    try:

        print("开始识别路由：", human_message)
        print("\n\n\n\\n")

        # 系统对话保存历史
        # res: ChatCompletionResponse = await client.chat(
        #     model="proxyllm",
        #     messages=human_message,
        #     conv_uid=conv_uid
        # )
        # ai_message = res.choices[0].message.content

        prompt = ChatPromptTemplate.from_messages([
            ("system", "你是一个内容专家，现在有以下应用：\n"
                       "\t应用列表：{apps}\n"
                       "\t请根据我输入的内容识别我的意图，根据意图匹配需要使用哪个应用。\n"
                       "\t如果意图匹配成功：必须按照'{resp_template}'格式回复给我并且不要回复多余内容。\n"
                       "\t如果识别不到我的意图：以普通AI助手的身份回答我的问题。\n"
             ),
            ("human", "{human_input}")
        ])
        resp_template = (json.dumps({"app_code": "the value of app_code", "app_descpibe": "the value of app_name"})
                         .replace("'", "\""))
        chain = LLMChain(llm=llm, prompt=prompt)
        apps_str = json.dumps(apps, ensure_ascii=False)
        ai_resp = chain.invoke({"apps": apps_str, "resp_template": resp_template, "human_input": human_message})
        ai_message = ai_resp['text']
        app_code = None
        app_descpibe = None
        print("路由识别结果：", ai_message)
        match = re.search(r"\{.*?\}", ai_message)
        response_text = ""
        strutured_message = None
        if match:
            strutured_message = match.group()
        print("路由解析结果：", strutured_message)

        code_key = "/router_app_code/" + conv_uid
        descpibe_key = "/router_app_descpibe/" + conv_uid
        if strutured_message and strutured_message != "None":
            print("开始加载strutured_message：", strutured_message)
            try:
                strutured_message = strutured_message.replace("'", "\"")
                dic = json.loads(strutured_message)
                app_code = dic["app_code"]
                app_descpibe = dic["app_descpibe"]
                cli = RedisClient()
                cli.set(code_key, app_code, 5 * 60)
                cli.set(descpibe_key, app_descpibe, 5 * 60)
                print("设置应用缓存：", code_key, app_code, app_descpibe)
            except Exception as e:
                print("解析应用失败:", e)
                raise e
        else:
            cli = RedisClient()
            app_code = cli.get(code_key)
            app_descpibe = cli.get(descpibe_key)
            print("查询应用缓存：", code_key, app_code, app_descpibe)
        print("当前应用：", app_code, app_descpibe)
        if app_code != None and app_code != "":
            dic = json.loads(strutured_message.replace("'", "\""))
            app_code = dic["app_code"]
            to_agent_message = human_message
            print("to_agent_message", to_agent_message)
            response_text = await call_agent(conv_uid,app_code,to_agent_message)
            print("发送智能体回复的消息：", response_text)
            larkutil.send_message(
                receive_id=conv_uid,
                content={"text": response_text},
                receive_id_type="open_id"
            )

        else:
            larkutil.send_message(
                receive_id=conv_uid,
                content={"text": ai_message},
                receive_id_type="open_id"
            )
    except Exception as e:
        logging.exception("服务器异常：", e)
        raise e
    return "OK"


async def call_agent(conv_uid, app_code, msg):
    response_text = ""
    DBGPT_API_KEY = ""
    client = Client(api_key=DBGPT_API_KEY)
    async for data in client.chat_stream(
            messages=msg,
            model="proxyllm",
            chat_mode="chat_app",
            chat_param=app_code,
            conv_uid=conv_uid

    ):
        try:
            content = data.choices[0].delta.content
            print("智能体响应结果：", content)
            response_text = content
            print("循环响应结果：", response_text)
        except Exception as e:
            logging.exception("解析智能体视图异常：", e)
            continue
    print("发送智能体回复的消息：", response_text)
    return response_text

# if (ai_message.startswith("{'app_code'")):
#     larkutil.send_message(
#         receive_id=conv_uid,
#         content={
#             "type": "template",
#             "data": {
#                 "template_id": "AAqkwmwOTohjy", "template_version_name": "1.0.10",
#                 "template_variable": {
#                     "ai_message": "请提供完整的信息！"
#                 }
#             }
#         },
#         receive_id_type="open_id",
#         msg_type="interactive"
#     )
