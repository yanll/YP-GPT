from typing import List, Dict
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dbgpt.extra.dag.buildin_awel.langgraph.tools.daily_push_message_tool import Dailypushmessagetool
from dbgpt.core.awel import DAG, HttpTrigger, MapOperator
from dbgpt.extra.dag.buildin_awel.lark import card_templates
from dbgpt.util.azure_util import create_azure_llm
from dbgpt.util.lark import lark_message_util  # 导入发送卡片的工具类
import json

# Create FastAPI instance
app = FastAPI()

# Instantiate original tool class
daily_push_tool = Dailypushmessagetool()

# Predefined conv_id list
conv_ids = [
    "ou_9d42bb88ec8940baf3ad183755131881",
    "ou_a22698cffd738d7851ef30f5dad1a06c",

]


class RequestHandleOperator(MapOperator[None, List[Dict]]):
    llm = None

    def __init__(self, **kwargs):
        self.llm = create_azure_llm()
        super().__init__(**kwargs)



    async def map(self, input_value: None) -> List[Dict]:
        results = []
        for conv_id in conv_ids:
            print(f"Receive conv_id: {conv_id}")
            try:
                result = daily_push_tool._run(conv_id=conv_id)
                results.append(result)
                # 获取_run函数返回的数据
                data = result.get("data", {})
                if not data:
                    logging.error(f"No data returned from _run function for conv_id {conv_id}")
                    continue
                # 发送卡片消息
                lark_message_util.send_card_message(
                    receive_id=conv_id,  # 使用 conv_id 作为接收者的 ID
                    content=card_templates.crem_sales_details_content(
                        template_variable={
                            "unlike_callback_event": {
                                "event_type": "unlike",
                                "event_source": "daily_push_message_list_card",
                                "event_data": {
                                    "message": "人员分级销售详情展示"
                                }
                            },
                            "query_str": data["query_str"],
                            "daily_push_message_list": data["list"],
                            "sales_diapaly": data["sales_diapaly"]
                        }
                    )
                )
                #results.append({"conv_id": conv_id, "send_card_response": resp})  # 将发送结果添加到结果列表中

            except Exception as e:
                logging.error(f"Error occurred while handling daily push event for conv_id {conv_id}: {e}")
                results.append({"conv_id": conv_id, "error": str(e)})
        return results


with DAG("dbgpt_awel_lark_daily_push_event") as dag:
    trigger = HttpTrigger(
        endpoint="/lark_daily_push_event",
        methods="POST",
        request_body=Dict
    )
    map_node = RequestHandleOperator()
    trigger >> map_node


# from typing import List, Dict
# import logging
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from dbgpt.extra.dag.buildin_awel.langgraph.tools.daily_push_message_tool import Dailypushmessagetool
# from dbgpt.core.awel import DAG, HttpTrigger, MapOperator
# from dbgpt.util.azure_util import create_azure_llm
# import json
#
# # Create FastAPI instance
# app = FastAPI()
#
# # Instantiate original tool class
# daily_push_tool = Dailypushmessagetool()
#
# # Predefined conv_id list
# conv_ids = [
#     "ou_9d42bb88ec8940baf3ad183755131881",
#     "ou_9d42bb88ec8940baf3ad183755131881",
#     "ou_9d42bb88ec8940baf3ad183755131881",
#     "ou_9d42bb88ec8940baf3ad183755131881"
#
# ]
#
# class RequestHandleOperator(MapOperator[None, List[Dict]]):
#     llm = None
#
#     def __init__(self, **kwargs):
#         self.llm = create_azure_llm()
#         super().__init__(**kwargs)
#
#     async def map(self, input_value: None) -> List[Dict]:
#         results = []
#         for conv_id in conv_ids:
#             print(f"Receive conv_id: {conv_id}")
#             try:
#                 result = daily_push_tool._run(conv_id=conv_id)
#                 results.append(result)
#             except Exception as e:
#                 logging.error(f"Error occurred while handling daily push event for conv_id {conv_id}: {e}")
#                 results.append({"conv_id": conv_id, "error": str(e)})
#         return results
#
# with DAG("dbgpt_awel_lark_daily_push_event") as dag:
#     trigger = HttpTrigger(
#         endpoint="/lark_daily_push_event",
#         methods="POST",
#         request_body=Dict
#     )
#     map_node = RequestHandleOperator()
#     trigger >> map_node
#
#
