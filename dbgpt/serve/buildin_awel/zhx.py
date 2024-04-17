import json
import logging
from typing import Dict
import asyncio
from dbgpt.client import Client

from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from dbgpt.util import larkutil
from dbgpt.util.azure_util import create_azure_llm
from dbgpt.core.awel import DAG, HttpTrigger, MapOperator
from collections import Counter

DBGPT_API_KEY = ""
# client = create_azure_llm()  # 假设 create_azure_llm 返回的是 Client 类型的实例
client = Client(api_key=DBGPT_API_KEY)
module_params = {
    "1": "f6198b70-f090-11ee-873c-005056b87963",  # 1.数据分析助手：
    "2": "65a31c88-e784-11ee-a738-1a4801a01981",  # 2.需求收集助手：
    "3": "2aa8eb96-f0d3-11ee-8eb3-1a4801a01981",  # 3.会议预定助手

    "4": "5b9491d6-edb0-11ee-97a3-1a4801a01981",  # 4.搜索助手
    "5": "aa262a16-e66d-11ee-ac1b-005056b87963",  # 5.代码生成助手
    "6": "f885dd70-e4f4-11ee-8b87-1a4801a01981"  # 6.交易数据分析助手

}


class RequestHandleOperator(MapOperator[Dict, str]):
    llm = None

    def __init__(self, **kwargs):
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
            await determine_message_type(self.llm, content_text)

            if message_type == "text" and sender_open_id != "" and content_text != "" and chat_type == "p2p":
                asyncio.create_task(handle(self.llm, sender_open_id, content_text))
                # rs = await determine_message_type(self.llm, content_text)
                # print("执行结果：", rs)
            return {"message": "OK"}
        except Exception as e:
            logging.exception("飞书事件处理异常！", e)
            return {"message": "OK"}


async def determine_message_type(llm, text_content):
    # 设置提示模板
    prompt = PromptTemplate(
        template="你是一个内容专家，现在有6个工具：【1：数据分析助手，2：需求收集助手，3：会议预定助手，4.搜索助手，5：代码生成助手，6：交易数据分析助】，请根据我输入的内容识别我的意图，根据意图匹配需要使用哪个工具，将工具编号回复给我，只回复编号，不要回复其他内容。如果识别不到我的意图，按照通用AI回复。以下是我的输入：'{msg}'",
        input_variables=["msg"]
    )
    # 创建处理链
    chain = LLMChain(llm=llm, prompt=prompt)
    # 发起调用
    response = chain.invoke({"msg": text_content})
    # 解析响应文本
    result = response["text"].strip()  # 假设返回的字典中包含 'text' 键
    # 提取所有数字并转换为整数
    numbers = [int(s) for s in result.split() if s.isdigit()]

    # 计算数字的频率
    if numbers:
        frequency = Counter(numbers)
        # 找到出现频率最高的数字
        most_common_number = frequency.most_common(1)[0][0]  # (数字, 频率)的元组，我们需要第一个元素
        # 判断数字是否在1-6之间
        if 1 <= most_common_number <= 6:
            return most_common_number
        else:
            return 0
    else:
        return 0


async def handle(llm, sender_open_id, human_message):
    message_type = await determine_message_type(llm, human_message)
    print(f"处理 {sender_open_id} 的消息，消息类型为：{message_type}")
    # # 初始化 response_text 为默认值
    # response_text = {"text": "未能识别意图或处理请求"}

    if message_type == 0 or message_type == None:
        prompt = PromptTemplate(
            template="{msg}",
            input_variables=["msg"]
        )
        chain = LLMChain(llm=llm, prompt=prompt)
        ai_message = chain.invoke({"msg": human_message})
        response_text = {"text": human_message + "：\n\n" + ai_message["text"]}
        print("使用默认LLM模型进行回应")
    else:
        app_id = module_params.get(str(message_type))
        if app_id is None:
            print(f"未找到与消息类型 {message_type} 相关的APP_ID")
            return

        async for data in client.chat_stream(
                messages=human_message,
                model="chatgpt_proxyllm",
                chat_mode="chat_app",
                chat_param=app_id,
                conv_uid="ef54fca2-5295-493e-8fd3-a966b581ac63"

        ):
            try:
                # 访问 choices 属性
                content = data.choices[0].delta.content
                agent_messages_json = content.split("```agent-messages\\n")[1].split("\\n```")[0]
                agent_messages_json = agent_messages_json.replace("\\\"", "\"")
                agent_messages = json.loads(agent_messages_json)
                markdown_text = agent_messages[0]['markdown']
                response_text = {"text": markdown_text}
                print(response_text)
            except Exception as e:
                print("Error extracting markdown text:", str(e))
                continue
            print('ddddddddd')
            print(f"使用APP_ID {app_id} 处理，对应的功能为：{message_type}")

    larkutil.send_message(
        receive_id=sender_open_id,
        content=response_text,
        receive_id_type="open_id"
    )


with DAG("dbgpt_awel_zhx") as dag:
    trigger = HttpTrigger(
        endpoint="/zhx",
        methods="POST",
        request_body=Dict
    )
    map_node = RequestHandleOperator()
    trigger >> map_node
