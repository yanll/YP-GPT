import logging
from typing import Dict

from dbgpt._private.pydantic import BaseModel, Field
from dbgpt.core.awel import DAG, HttpTrigger, MapOperator
from dbgpt.extra.dag.buildin_awel.hanglv.airline_monitor_push4 import AirlineMonitorPush4
from dbgpt.extra.dag.buildin_awel.hanglv.hanglv1_1 import monitor_one
from dbgpt.extra.dag.buildin_awel.hanglv.hanglv1_2 import monitor_one2
from dbgpt.extra.dag.buildin_awel.hanglv.hanglv2 import monitor_two
from dbgpt.extra.dag.buildin_awel.hanglv.hanglv3 import monitor_three


class TriggerReqBody(BaseModel):
    switch_monitor1_1: str = Field(default="")
    switch_monitor1_2: str = Field(default="")
    switch_monitor2: str = Field(default="")
    switch_monitor3: str = Field(default="")
    switch_monitor4: str = Field(default="")


class RequestHandleOperator(MapOperator[Dict, str]):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def map(self, input_value: TriggerReqBody) -> dict:

        results = []
        if input_value.switch_monitor1_1 == "true":
            try:
                result = monitor_one()
                results.append(result)
            except Exception as e:
                logging.error(f"Error occurred while executing monitor_two: {e}")
                results.append(f"Monitor four failed: {str(e)}")

        if input_value.switch_monitor1_2 == "true":
            try:
                result = monitor_one2()
                results.append(result)
            except Exception as e:
                logging.error(f"Error occurred while executing monitor_two: {e}")
                results.append(f"Monitor four failed: {str(e)}")

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
                monitor_four_class = AirlineMonitorPush4()
                result = monitor_four_class.run_push()
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
