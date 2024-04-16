import json
import logging
from typing import Dict
import asyncio

from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from dbgpt.util import larkutil
from dbgpt.util.azure_util import create_azure_llm
from dbgpt.core.awel import DAG, HttpTrigger, MapOperator
from collections import Counter

DBGPT_API_KEY = "1345"
client = create_azure_llm()  # 假设 create_azure_llm 返回的是 Client 类型的实例
module_params = {
    "1": "f6198b70-f090-11ee-873c-005056b87963",
    "2": "e66e7120-e778-11ee-94fd-005056b87963",
    "3": "cbf058e0-e778-11ee-94fd-005056b87963",
    "4": "c3514700-e66d-11ee-ac1b-005056b87963",
    "5": "aa262a16-e66d-11ee-ac1b-005056b87963",
    "6": "6e1a9bce-e66d-11ee-ac1b-005056b87963"
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

            if message_type == "text" and sender_open_id != "" and content_text != "" and chat_type == "p2p":
                # asyncio.create_task(handle(self.llm, sender_open_id, content_text))
                rs = await determine_message_type(self.llm, content_text)
                print("执行结果：", rs)
            return {"message": "OK"}
        except Exception as e:
            logging.exception("飞书事件处理异常！", e)
            return {"message": "OK"}


async def determine_message_type(llm, text_content):
    # 设置提示模板
    prompt = PromptTemplate(
        template="现在我会给你发一段话：'{msg}'，你需要理解我这段话的意思，然后从我的几个功能中选择一个，功能代号与名字如下功能1.数据分析助手：2.需求收集助手,3.会议预定助手的5.代码生成助手6.交易数据分析助手，然后输出对应功能的数字。",
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
    # 如果未提取到数字，默认返回0
    if not numbers:
        return 0
    # 计算数字出现频率并找到最常见的数字
    counts = Counter(numbers)
    most_common_number = counts.most_common(1)[0][0]
    # 检查数字是否在1到6之间
    if 1 <= most_common_number <= 6:
        return most_common_number
    # 如果没有有效数字，返回默认响应指示
    return "generate_response"


async def handle(llm, sender_open_id, human_message):
    message_type = await determine_message_type(client, human_message)
    print(f"处理 {sender_open_id} 的消息，消息类型为：{message_type}")

    if message_type == 0 or message_type == "generate_response":
        prompt = PromptTemplate(
            template="{msg}",
            input_variables=["msg"]
        )
        chain = LLMChain(llm=client, prompt=prompt)
        ai_message = chain.invoke({"msg": human_message})
        response_text = {"text": human_message + "：\n\n" + ai_message["text"]}
        print("使用默认LLM模型进行回应")
    else:
        app_id = module_params.get(str(message_type))
        if app_id is None:
            print(f"未找到与消息类型 {message_type} 相关的APP_ID")
            return

        async for data in client.chat_stream(
                messages=[human_message],
                model="chatgpt_proxyllm",
                chat_mode="chat_app",
                chat_param=app_id):
            response_text = data['choices'][0]['delta']['content']
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
