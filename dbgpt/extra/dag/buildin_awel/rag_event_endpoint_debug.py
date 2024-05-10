import asyncio
import logging
from typing import Dict

from dbgpt.core.awel import DAG, HttpTrigger, MapOperator
from dbgpt.extra.dag.buildin_awel.lark.lark_event_handler import LarkEventHandler
from dbgpt.extra.dag.buildin_awel.lark.rag_event_handler import RAGLarkHandler


class RequestHandleOperator(MapOperator[Dict, str]):

    def __init__(self, **kwargs):
        self.lark_event_handler = LarkEventHandler()
        self.rag_event_handler = RAGLarkHandler()
        super().__init__(**kwargs)

    async def map(self, input_body: Dict) -> Dict:
        try:
            print(f"接收飞书事件debug: {input_body}")
            # 首次验证挑战码
           
            asyncio.create_task(
                self.rag_event_handler.debug_handle(input_body)
            )
            print("before return.....")
            return {}
        except Exception as e:
            logging.exception("飞书事件处理异常！", e)
            return {}


with DAG("dbgpt_awel_ragdebug_event_endpoint") as dag:
    trigger = HttpTrigger(
        endpoint="/ragdebug_event_endpoint",
        methods="POST",
        request_body=Dict
    )

    map_node = RequestHandleOperator()
    trigger >> map_node
