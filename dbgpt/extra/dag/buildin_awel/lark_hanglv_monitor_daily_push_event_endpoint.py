from typing import Dict
from dbgpt.core.awel import DAG, HttpTrigger, MapOperator
import logging

from dbgpt.extra.dag.buildin_awel.hanglv3 import monitor_three
# 假设 monitor_four 和 monitor_two 函数定义在 dbgpt.extra.dag.buildin_awel.hanglv4 模块中
from dbgpt.extra.dag.buildin_awel.hanglv4 import monitor_four
from dbgpt.extra.dag.buildin_awel.hanglv2 import monitor_two
import logging
from typing import List, Dict

import requests
from fastapi import FastAPI

from dbgpt.core.awel import DAG, HttpTrigger, MapOperator
from dbgpt.extra.dag.buildin_awel.langgraph.tools.daily_push_message_tool import Dailypushmessagetool
from dbgpt.extra.dag.buildin_awel.lark import card_templates
from dbgpt.util.azure_util import create_azure_llm
from dbgpt.util.lark import lark_message_util  # 导入发送卡片的工具类
from dbgpt.util.lark import larkutil

class RequestHandleOperator(MapOperator[Dict, str]):
    llm = None

    def __init__(self, **kwargs):
        self.llm = create_azure_llm()
        super().__init__(**kwargs)

    async def map(self, input_value: Dict) -> str:

        results = []


        #monitor_two
        try:
            result = monitor_two()
            results.append(result)

        except Exception as e:
            logging.error(f"Error occurred while executing monitor_two: {e}")
            results.append(f"Monitor four failed: {str(e)}")

        # monitor_three
        try:
            result = monitor_three()
            results.append(result)

        except Exception as e:
            logging.error(f"Error occurred while executing monitor_three: {e}")
            results.append(f"Monitor four failed: {str(e)}")

        #monitor_four
        try:
            result = monitor_four()
            results.append(result)

        except Exception as e:
            logging.error(f"Error occurred while executing monitor_four: {e}")
            results.append(f"Monitor four failed: {str(e)}")


with DAG("dbgpt_awel_lark_hanglv_monitor_daily_push_event") as dag:
    trigger = HttpTrigger(
        endpoint="/lark_hanglv_monitor_daily_push_event",
        methods="POST",
        request_body=Dict
    )
    map_node = RequestHandleOperator()
    trigger >> map_node

