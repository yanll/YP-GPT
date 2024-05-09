import logging
from typing import Optional, Type
from typing import List

from langchain.tools import BaseTool
from langchain_core.callbacks import (
    CallbackManagerForToolRun,
)
from pydantic import BaseModel, Field

from dbgpt.extra.dag.buildin_awel.lark import card_templates
from dbgpt.util.lark import larkutil, lark_card_util, lark_message_util


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

    # industry_line: str = Field(
    #     name="所属行业线",
    #     description="所属行业线",
    #     default=""
    # )
    customer_role: str = Field(
        name='客户角色',
        description='客户角色，' + lark_card_util.card_options_to_input_field_description(
                        lark_card_util.card_options_for_customer_role()
                    ),
    )
    customer_source_default: str = Field(
        name="客户来源",
        description="客户来源, " + lark_card_util.card_options_to_input_field_description(
                        lark_card_util.card_options_for_customer_source()
                    ),
        default=""
    )
    customer_importance_default: str = Field(
        name="客户重要程度",
        description="客户重要程度, " + lark_card_util.card_options_to_input_field_description(
                        lark_card_util.card_options_for_customer_importance()
                    ),
        default=""
    )


class CrmBusCustomerCollectTool(BaseTool):
    name: str = "crm_bus_customer_collect_tool"
    description: str = (
        "这是一个报单客户信息填写工具，帮助销售用户填写报单客户信息。"
        "当需要填写报单客户时非常有用。 "
        "能够尽可能全的收集报单信息。"
        "调用本工具需要的参数值均来自用户的输入，可以默认为空，但是禁止随意编造。"
        ""
    )
    args_schema: Type[BaseModel] = CrmBusCustomerCollectInput

    def _run(
            self,
            conv_id: str = "",
            customer_name: str = "",
            customer_role: str = "",
            customer_source_default: str = "",
            customer_importance_default: str = ""
    ):
        """Use the tool."""
        print("开始运行添加报单客户信息填写工具：", conv_id, customer_name, customer_role, customer_source_default,
              customer_importance_default)
        try:
            if customer_name == "":
                resp = {"success": "false", "response_message": "the name of customer"}
            elif customer_role == "":
                resp = {"success": "false", "response_message": "the industry line of customer"}
            else:
                resp = do_collect(
                    conv_id=conv_id,
                    customer_name=customer_name,
                    customer_role=customer_role,
                    customer_source_default=customer_source_default,
                    customer_importance_default=customer_importance_default
                )
            return resp
        except Exception as e:
            logging.error("工具运行异常：", e)
            return repr(e)


def do_collect(
        conv_id: str = "",
        customer_name: str = "",
        customer_role: str = "",
        customer_source_default: str = "",
        customer_importance_default: str = ""
):
    """
    处理并收集提报信息，返回收集结果。
    """
    try:
        """
        我要填写报单客户：
        客户名：转转精神。
        客户角色：标准商户
        客户来源：朋友介绍
        客户重要程度：一般商户
        """
        print("发送飞书提报卡片：", conv_id)
        lark_message_util.send_message(
            receive_id=conv_id,
            content=card_templates.create_crm_bus_customer_card_content(
                template_variable={
                    "card_metadata": {
                        "card_name": "crm_bus_customer_collect",
                        "description": "添加报单客户信息表单"
                    },
                    "customer_name": customer_name,
                    "customer_role": lark_card_util.get_action_index_by_text_from_options(
                        customer_role,
                        lark_card_util.card_options_for_customer_role()
                    ),
                    "customer_source_default": lark_card_util.get_action_index_by_text_from_options(
                        customer_source_default,
                        lark_card_util.card_options_for_customer_source()
                    ),
                    "customer_importance_default": lark_card_util.get_action_index_by_text_from_options(
                        customer_importance_default,
                        lark_card_util.card_options_for_customer_importance()
                    ),


                    "customer_role_options": lark_card_util.card_options_for_customer_role(),
                    "customer_source_options": lark_card_util.card_options_for_customer_source(),
                    "customer_importance_options": lark_card_util.card_options_for_customer_importance()
                }
            ),
            receive_id_type="open_id",
            msg_type="interactive"
        )
    except Exception as e:
        logging.error("飞书添加报单客户信息卡片发送失败：", e)

    # 创建并返回结果字典
    return {
        "success": "true",
        "error_message": "",
        "display_type": "form",
        # "data": {
        #     "conv_id": conv_id,
        #     "daily_report_content": daily_report_content,
        #     "create_date": create_date,
        #     "daily_report_tomorrow_plans": plans_description,
        #     "senders_name": senders_name
        # }
    }
