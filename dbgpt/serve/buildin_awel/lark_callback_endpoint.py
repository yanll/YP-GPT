import json
import logging
import os
from typing import Dict

from langchain_openai import AzureChatOpenAI

from dbgpt.core.awel import DAG, HttpTrigger, MapOperator
from dbgpt.util.azure_util import create_azure_llm


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

            return {
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
                        "template_id": "AAqkwmwOTohjy", "template_version_name": "1.0.8",
                        "template_variable": {
                            "ai_message": "请提供完整的信息！"
                        }
                    }
                }
            }
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
