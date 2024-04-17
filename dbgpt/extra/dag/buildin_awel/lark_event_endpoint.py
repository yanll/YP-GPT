import asyncio
import json
import logging
from typing import Dict, List
import re
from langchain_core.messages import HumanMessage
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
            if message_type == "text" and sender_open_id != "" and content_text != "" and chat_type == "p2p":
                asyncio.create_task(
                    request_handle(apps, self.llm, self.chat_history_message_dao, sender_open_id, content_text)
                )
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

    graph = MessageGraph()
    graph.add_node("call_extract_app", call_extract_app)
    graph.add_edge("call_extract_app", END)
    graph.set_entry_point("call_extract_app")
    runnable = graph.compile()
    messages = []
    his_: List[ChatHistoryMessageEntity] = chat_history_dao.get_his_messages_by_uid(sender_open_id)
    his: List[ChatHistoryMessageEntity] = []
    role_desc = (
        f"你是一个智能助手，现在有以下应用：\n"
        f"{json.dumps(apps, ensure_ascii=False)}\n"
        "请根据我输入的内容识别我的意图，根据意图匹配需要使用哪个应用，如果意图匹配成功则按照：{'app_code': 'the value of app_code', 'app_descpibe': 'the value of app_descpibe'}格式回复给我（不要回复多余内容），否则按照通用AI角色回复我的问题。\n"
        "\n"
    )
    "以下是我和AI的对话内容：\n"
    "\n\n"

    messages.append(HumanMessage(name=sender_open_id, content="system:" + role_desc))
    if his:
        for m in his:
            dict = json.loads(m.message_detail)
            if dict["type"] == "human":
                messages.append(HumanMessage(name=sender_open_id, content="human:" + dict["data"]["content"]))
            if dict["type"] == "ai":
                messages.append(HumanMessage(name=sender_open_id, content="ai:" + dict["data"]["content"]))
    messages.append(HumanMessage(name=sender_open_id, content="human:" + human_message))
    await runnable.ainvoke(messages)


async def call_extract_app(messages: List[HumanMessage]):
    try:
        DBGPT_API_KEY = ""
        client = Client(api_key=DBGPT_API_KEY)
        mess = []
        conv_uid = messages[0].name
        for m in messages:
            mess.append(m.content + "\n")
        res: ChatCompletionResponse = await client.chat(
            model="proxyllm",
            messages="".join(mess),
            conv_uid=conv_uid
        )
        ai_message = res.choices[0].message.content
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
        print("当前应用：", app_descpibe)
        if app_code != None and app_code != "":
            dic = json.loads(strutured_message.replace("'", "\""))
            app_code = dic["app_code"]
            to_agent_message = messages[-1].content.replace("human:", "")
            print("to_agent_message", to_agent_message)
            async for data in client.chat_stream(
                    messages=to_agent_message,
                    model="proxyllm",
                    chat_mode="chat_app",
                    chat_param=app_code,
                    conv_uid=conv_uid

            ):
                try:

                    content = data.choices[0].delta.content
                    print("智能体响应结果：", content)
                    # agent_messages_json = content.split("```agent-messages\\n")[1].split("\\n```")[0]
                    # agent_messages_json = agent_messages_json.replace("\\\"", "\"")
                    # agent_messages = json.loads(agent_messages_json)
                    # markdown_text = agent_messages[0]['markdown']
                    # response_text = markdown_text
                    response_text = content
                    print("循环响应结果：", response_text)
                except Exception as e:
                    logging.exception("解析智能体视图异常：", e)
                    continue
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
