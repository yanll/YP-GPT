import logging
from typing import Optional, Type
from typing import List

from langchain.tools import BaseTool
from langchain_core.callbacks import (
    CallbackManagerForToolRun,
)
from pydantic import BaseModel, Field

from dbgpt.extra.dag.buildin_awel.langgraph.wrappers.crem_api_wrapper import get_crm_user_industry_line, \
    get_crm_user_name, query_crm_bus_customer
from dbgpt.extra.dag.buildin_awel.langgraph.wrappers.lark_event_handler_wrapper import LarkEventHandlerWrapper
from dbgpt.extra.dag.buildin_awel.lark import card_templates
from dbgpt.util.lark import lark_message_util, lark_card_util


class CrmBusCustomerCollectInput(BaseModel):
    """

    """
    conv_id: str = Field(
        name="conv_id",
        description="the value of conv_id",
    )
    customer_name: str = Field(
        name="客户名称",
        description="客户名称",
        default=""
    )
    customer_service_levels: str = Field(
        name="客户等级",
        description="客户等级, " + lark_card_util.card_options_to_input_field_description(
            lark_card_util.card_options_for_customer_service_levels()),
        default=""
    )

    sale_name: str = Field(
        name="销售名字",
        description="销售名字",
        default=""
    )

    customer_source_default: str = Field(
        name="客户来源",
        description="客户来源, " + lark_card_util.card_options_to_input_field_description(
            lark_card_util.card_options_for_customer_source()
        ),
        default=""
    )


class CrmBusCustomerCollectQueryTool(BaseTool):
    name: str = "crm_bus_customer_collect_tool"
    description: str = (
        "这是一个查询报单工具，帮助销售用户查询报单客户信息。"
        "当需要查询报单客户时非常有用。 "
        "能够尽可能全的收集报单信息。"
        "调用本工具需要的参数值均来自用户的输入，可以默认为空，但是禁止随意编造。"
        ""
    )
    args_schema: Type[BaseModel] = CrmBusCustomerCollectInput

    def _run(
            self,
            conv_id: str = "",
            customer_name: str = "",
            customer_service_levels: str = "",
            sale_name: str = "",
            customer_source_default: str = "",
    ):
        """Use the tool."""
        print("开始运行查询报单客户信息工具：", conv_id, customer_name, customer_source_default,
              )
        try:
            resp = query_crm_bus_customer(open_id=conv_id, data={})
            lark_event_handler_wrapper = LarkEventHandlerWrapper()
            # if isinstance(resp, str):
            #     lark_event_handler_wrapper.lark_reply_general_message(sender_open_id=conv_id, resp_msg=resp)
            # else:
            #     lark_event_handler_wrapper.lark_reply_general_message(sender_open_id=conv_id, resp_msg='查询信息')

            return resp
        except Exception as e:
            logging.error("工具运行异常：", e)
            return repr(e)
