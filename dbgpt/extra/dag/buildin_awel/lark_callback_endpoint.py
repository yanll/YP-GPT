import asyncio
import json
import logging
import os
from typing import Dict

from langchain_openai import AzureChatOpenAI

from dbgpt.core.awel import DAG, HttpTrigger, MapOperator
from dbgpt.util.azure_util import create_azure_llm
from datetime import datetime
from dbgpt.util import larkutil


class RequestHandleOperator(MapOperator[Dict, str]):
    llm = None

    def __init__(self, **kwargs):
        self.llm = create_azure_llm()
        super().__init__(**kwargs)

    async def map(self, input_body: Dict) -> str:
        try:
            print(f"接收飞书回调: {input_body}")
            # 首次验证挑战码
            if "challenge" in input_body:
                return {"challenge": input_body["challenge"]}

            print("开始异步执行回调", input_body)
            asyncio.create_task(
                request_handle(input_body)
            )
            print("执行日志", input_body)


        except Exception as e:
            logging.exception("飞书回调处理异常！", e)
            return {"message": "OK"}


with DAG("dbgpt_awel_lark_callback_endpoint") as dag:
    trigger = HttpTrigger(
        endpoint="/lark_callback_endpoint",
        methods="POST",
        request_body=Dict
    )
    map_node = RequestHandleOperator()
    trigger >> map_node


async def request_handle(input_body: Dict):
    print("lark_callback_endpoint async handle：", input_body)
    form_value = input_body['event']['action']['form_value']

    rs = {
        "toast": {
            "type": "info",
            "content": "温馨提示",
            "i18n": {
                "zh_cn": "信息已提交，请查看结果！",
                "en_us": "submitted"
            }
        },
        "card": {
            "type": "template",
            "data": {
                "template_id": "AAqkwmwOTohjy", "template_version_name": "1.0.10",
                "template_variable": {
                    "ai_message": "请提供完整的信息！"
                }
            }
        }
    }
    print("LarkCallbackHandleResult:", "")
    return rs
