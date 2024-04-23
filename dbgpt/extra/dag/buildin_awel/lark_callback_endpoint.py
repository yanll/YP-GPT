import asyncio
import logging
from typing import Dict

from dbgpt.core.awel import DAG, HttpTrigger, MapOperator
from dbgpt.extra.dag.buildin_awel.langgraph.wrappers import lark_api_wrapper
from dbgpt.util.azure_util import create_azure_llm


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
            # asyncio.create_task(
            rs = request_handle(input_body)
            # )
            print("执行日志", input_body)
            return rs

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


def request_handle(input_body: Dict):
    print("lark_callback_endpoint async handle：", input_body)
    rs = lark_api_wrapper.handle_lark_callback(input_body)
    print("LarkCallbackHandleResult:", "")
    return rs
