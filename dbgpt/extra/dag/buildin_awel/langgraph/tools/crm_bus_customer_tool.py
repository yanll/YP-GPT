import logging
from typing import Optional, Type
from typing import List

from langchain.tools import BaseTool
from langchain_core.callbacks import (
    CallbackManagerForToolRun,
)
from pydantic import BaseModel, Field

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

    industry_line: str = Field(
        name="行业线",
        description="行业线， " + lark_card_util.card_options_to_input_field_description(
            lark_card_util.card_options_for_industry_line()
        ),
        default=""
    )

    business_type: str = Field(
        name="所属行业",
        description="所属行业",
        default=""
    )

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
    product_type: str = Field(
        name="产品形态",
        description="产品形态, " + lark_card_util.card_options_to_input_field_description(
            lark_card_util.card_options_for_product_type()
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
            industry_line: str = "",
            business_type: str = "",
            customer_role: str = "",
            customer_source_default: str = "",
            customer_importance_default: str = "",
            product_type: str = "",
    ):
        """Use the tool."""
        print("开始运行添加报单客户信息填写工具：", conv_id, customer_name, customer_role, customer_source_default,
              customer_importance_default)
        try:
            if industry_line == "":
                resp = {"success": "false", "response_message": "缺少行业线信息"}
            else:
                resp = do_collect(
                    conv_id=conv_id,
                    industry_line=industry_line,
                    business_type=business_type,
                    customer_name=customer_name,
                    customer_role=customer_role,
                    customer_source_default=customer_source_default,
                    customer_importance_default=customer_importance_default,
                    product_type=product_type
                )
            return resp
        except Exception as e:
            logging.error("工具运行异常：", e)
            return repr(e)


def do_collect(
        conv_id: str = "",
        customer_name: str = "",
        industry_line: str = "",
        business_type: str = "",
        customer_role: str = "",
        customer_source_default: str = "",
        customer_importance_default: str = "",
        product_type: str = "",
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
        if industry_line == "Web3.0行业线":
            lark_message_util.send_card_message(
                receive_id=conv_id,
                content=card_templates.create_crm_bus_customer_card_content.Web3(
                    template_variable={
                        "card_metadata": {
                            "card_name": "crm_bus_customer_collect",
                            "description": "添加报单客户信息表单"
                        },
                        "customer_name": customer_name,
                        # "business_type": 99,
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
                )
            )
        elif industry_line == "金融行业线":
            lark_message_util.send_card_message(
                receive_id=conv_id,
                content=card_templates.create_crm_bus_customer_card_content.Finance(
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
                        "business_type_options": lark_card_util.card_options_for_business_type.Finance(),
                        "customer_role_options": lark_card_util.card_options_for_customer_role(),
                        "customer_source_options": lark_card_util.card_options_for_customer_source(),
                        "customer_importance_options": lark_card_util.card_options_for_customer_importance()
                    }
                )
            )
        elif industry_line == "大零售行业线":
            lark_message_util.send_card_message(
                receive_id=conv_id,
                content=card_templates.create_crm_bus_customer_card_content.Retail(
                    template_variable={
                        "card_metadata": {
                            "card_name": "crm_bus_customer_collect",
                            "description": "添加报单客户信息表单"
                        },
                        "customer_name": customer_name,
                        # "business_type": business_type,
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
                        "product_type": lark_card_util.get_action_index_by_text_from_options(
                            customer_importance_default,
                            lark_card_util.card_options_for_product_type()
                        ),
                        "business_type_options": lark_card_util.card_options_for_business_type.Retail(),
                        "customer_role_options": lark_card_util.card_options_for_customer_role(),
                        "customer_source_options": lark_card_util.card_options_for_customer_source(),
                        "customer_importance_options": lark_card_util.card_options_for_customer_importance(),
                        "product_type_options": lark_card_util.card_options_for_product_type()
                    }
                )
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
