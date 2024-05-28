import logging
import json
from typing import Optional, Type
from typing import List

from langchain.tools import BaseTool
from langchain_core.callbacks import (
    CallbackManagerForToolRun,
)
from pydantic import BaseModel, Field

from dbgpt.extra.dag.buildin_awel.langgraph.wrappers.operation_rpa_api_wrapper import execute_rpa_task
from dbgpt.extra.dag.buildin_awel.langgraph.wrappers.lark_event_handler_wrapper import LarkEventHandlerWrapper
from dbgpt.extra.dag.buildin_awel.lark import card_templates
from dbgpt.util.lark import lark_message_util, lark_card_util
from dbgpt.util.lark.lark_card_util import get_value_by_text_from_options


class OpetationCheckOPROrderInput(BaseModel):
    """

    """
    conv_id: str = Field(
        name="conv_id",
        description="the value of conv_id",
    )
    order_number: str = Field(
        name="订单编号",
        description="订单编号",
        default=""
    )


class OpetationCheckOPROrderTool(BaseTool):
    name: str = "operating_check_opr_order_tool"
    description: str = (
        "opr订单查询，查询状态，根因等信息"
        "请注意：\n"
        "1、调用本工具需要的参数值来自用户输入，可以默认为空，但是禁止随意编造。\n"
        ""
    )
    args_schema: Type[BaseModel] = OpetationCheckOPROrderInput

    def _run(
            self,
            conv_id: str = "",
            order_number: str = ""
    ):
        """Use the tool."""
        print("开始拆讯opr订单信息", conv_id, order_number)
        try:
            resp = execute_rpa_task("OPEN_BAIDU")
            
            return {
                    "success": "true",
                    "error_message": "",
                    # "action": {
                    #     "action_name": "send_lark_form_card",
                    #     "card_name": "crm_bus_customer_query_result"
                    # },
                    "data": {
                        "conv_id": conv_id,
                        "content": json.dumps(resp)

                    }
                }
        except Exception as e:
            logging.error("工具运行异常：", e)
            return repr(e)
