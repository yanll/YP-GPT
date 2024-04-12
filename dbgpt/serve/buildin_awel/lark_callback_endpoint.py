import json
from typing import Dict

from dbgpt.core.awel import DAG, HttpTrigger, MapOperator


class RequestHandleOperator(MapOperator[Dict, str]):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def map(self, input_body: Dict) -> str:
        print(f"Receive input body: {input_body}")
        rs = "received message:" + json.dumps(input_body)
        return rs


with DAG("dbgpt_awel_lark_callback_endpoint") as dag:
    trigger = HttpTrigger(
        "/lark_callback_endpoint",
        methods="POST",
        request_body=Dict
    )
    map_node = RequestHandleOperator()
    trigger >> map_node
