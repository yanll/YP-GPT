import asyncio
import logging
from typing import Dict

from dbgpt.core.awel import DAG, HttpTrigger, MapOperator
from dbgpt.extra.dag.buildin_awel.lark.lark_callback_handler import LarkCallbackHandler
from dbgpt.util.azure_util import create_azure_llm


class RequestHandleOperator(MapOperator[Dict, str]):
    llm = None

    def __init__(self, **kwargs):
        self.llm = create_azure_llm()
        self.lark_callback_handler = LarkCallbackHandler()
        super().__init__(**kwargs)

    async def map(self, input_body: Dict) -> Dict:
        try:
            print(f"接收飞书回调: {input_body}")
            # 首次验证挑战码
            if "challenge" in input_body:
                return {"challenge": input_body["challenge"]}
            # asyncio.create_task(
            #     self.lark_callback_handler.a_handle(input_body)
            # )
            # return {}
            return await self.lark_callback_handler.a_handle(input_body)

        except Exception as e:
            logging.exception("飞书回调处理异常！", e)
            return {}


with DAG("dbgpt_awel_lark_callback_endpoint") as dag:
    trigger = HttpTrigger(
        endpoint="/lark_callback_endpoint",
        methods="POST",
        request_body=Dict
    )
    map_node = RequestHandleOperator()
    trigger >> map_node
