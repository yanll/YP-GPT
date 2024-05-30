import logging
from typing import Dict

from dbgpt._private.pydantic import BaseModel, Field
from dbgpt.core.awel import DAG, HttpTrigger, MapOperator
from dbgpt.extra.dag.buildin_awel.hanglv2 import monitor_two
from dbgpt.extra.dag.buildin_awel.hanglv3 import monitor_three
from dbgpt.extra.dag.buildin_awel.hanglv4 import monitor_four


class TriggerReqBody(BaseModel):
    switch_monitor1: str = Field(default="")
    switch_monitor2: str = Field(default="")
    switch_monitor3: str = Field(default="")
    switch_monitor4: str = Field(default="")


class RequestHandleOperator(MapOperator[Dict, str]):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def map(self, input_value: TriggerReqBody) -> dict:

        results = []
        if input_value.switch_monitor1 == "true":
            pass

        if input_value.switch_monitor2 == "true":
            try:
                result = monitor_two()
                results.append(result)
            except Exception as e:
                logging.error(f"Error occurred while executing monitor_two: {e}")
                results.append(f"Monitor four failed: {str(e)}")

        if input_value.switch_monitor3 == "true":
            try:
                result = monitor_three()
                results.append(result)

            except Exception as e:
                logging.error(f"Error occurred while executing monitor_three: {e}")
                results.append(f"Monitor four failed: {str(e)}")

        if input_value.switch_monitor4 == "true":
            try:
                result = monitor_four()
                results.append(result)

            except Exception as e:
                logging.error(f"Error occurred while executing monitor_four: {e}")
                results.append(f"Monitor four failed: {str(e)}")

        return {"status": "success"}


with DAG("dbgpt_awel_lark_hanglv_monitor_daily_push_event") as dag:
    print("开始监控推送")
    trigger = HttpTrigger(
        endpoint="/lark_hanglv_monitor_daily_push_event",
        methods="GET",
        request_body=TriggerReqBody
    )
    map_node = RequestHandleOperator()
    trigger >> map_node
