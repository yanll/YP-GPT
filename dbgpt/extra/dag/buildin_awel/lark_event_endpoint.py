import asyncio
import logging
from typing import Dict

from dbgpt.core.awel import DAG, HttpTrigger, MapOperator
from dbgpt.extra.dag.buildin_awel.lark.lark_event_handler import LarkEventHandler


class RequestHandleOperator(MapOperator[Dict, str]):

    def __init__(self, **kwargs):
        self.lark_event_handler = LarkEventHandler()
        super().__init__(**kwargs)

    async def map(self, input_body: Dict) -> Dict:
        try:
            print(f"接收飞书事件: {input_body}")
            # 首次验证挑战码
            if "challenge" in input_body:
                return {"challenge": input_body["challenge"]}
            if self.lark_event_handler.valid_event_type(input_body) is False:
                return {}
            if self.lark_event_handler.valid_repeat(input_body) is False:
                return {}
            asyncio.create_task(
                self.lark_event_handler.a_handle(input_body)
            )
            return {}
        except Exception as e:
            logging.exception("飞书事件处理异常！", e)
            return {}


with DAG("dbgpt_awel_lark_event_endpoint") as dag:
    trigger = HttpTrigger(
        endpoint="/lark_event_endpoint",
        methods="POST",
        request_body=Dict
    )

    map_node = RequestHandleOperator()
    trigger >> map_node
