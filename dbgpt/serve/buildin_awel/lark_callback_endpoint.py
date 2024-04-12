from typing import Optional

from dbgpt._private.pydantic import BaseModel, Field
from dbgpt.core.awel import DAG, HttpTrigger, MapOperator


class ReqContext(BaseModel):
    conv_uid: str = Field(..., description="会话标识")


class TriggerReqBody(BaseModel):
    pass


class RequestHandleOperator(MapOperator[TriggerReqBody, str]):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def map(self, input_body: TriggerReqBody) -> str:
        print(f"Receive input body: {input_body}")
        return "OK," + input_body


with DAG("dbgpt_awel_lark_callback_endpoint") as dag:
    trigger = HttpTrigger(
        "/lark_callback_endpoint",
        methods="POST",
        request_body=TriggerReqBody
    )
    map_node = RequestHandleOperator()
    trigger >> map_node
