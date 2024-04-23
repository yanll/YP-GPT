from typing import Dict

from dbgpt.core.awel import DAG, HttpTrigger, MapOperator
from dbgpt.util.azure_util import create_azure_llm


class RequestHandleOperator(MapOperator[Dict, str]):
    llm = None

    def __init__(self, **kwargs):
        self.llm = create_azure_llm()
        super().__init__(**kwargs)

    async def map(self, input_value: str) -> str:
        print(f"Receive input value: {input_value}")
        return f"Hello, your message is: {input_value}"


with DAG("dbgpt_awel_hello") as dag:
    trigger = HttpTrigger(
        endpoint="/hello",
        methods="GET",

        request_body=Dict
    )
    map_node = RequestHandleOperator()
    trigger >> map_node
