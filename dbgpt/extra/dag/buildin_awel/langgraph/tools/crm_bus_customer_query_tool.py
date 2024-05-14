import logging
import math
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
from dbgpt.util.lark.lark_card_util import get_value_by_text_from_options


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

    customer_importance: str = Field(
        name="客户重要程度",
        description="客户重要程度, " + lark_card_util.card_options_to_input_field_description(
            lark_card_util.card_options_for_customer_importance()
        ),
        default=""
    )

    display_number: int = Field(
        name="展示查询结果的个数",
        description="展示查询结果的个数",
        default=5
    )


class CrmBusCustomerCollectQueryTool(BaseTool):
    name: str = "crm_bus_customer_collect_tool"
    description: str = (
        "这是一个查询报单的工具，帮助用户查询报单信息。"
        "注意只是查询。填写报单是另一个工具 "
        "调用本工具需要的参数值可以默认为空，但是禁止随意编造。"
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
            customer_importance: str = "",
            display_number: int = 5,
    ):
        """Use the tool."""
        print("开始运行查询报单客户信息工具：", conv_id, customer_name, customer_source_default,
              )
        try:
            resp = query_crm_bus_customer(open_id=conv_id, data={
                "customerName": customer_name,
                "customerServiceLevels": lark_card_util.get_value_by_text_from_options(customer_service_levels,
                                                                                       lark_card_util.card_options_for_customer_service_levels()),
                "saleName": sale_name,
                "customerImportance": customer_importance,
                "tabType": "全部",
                "customerSource": customer_source_default,
                "pageNum": 1,
                "pageSize": 1000,
            })
            if isinstance(resp, str):
                return resp
            else:
                query_result_summary = f'查询到{len(resp)}个结果，展示{min(len(resp), display_number)}个结果。'
                query_iteria = ''
                if customer_name != '':
                    query_iteria += f'客户名称:{customer_name};'
                if customer_service_levels != '':
                    query_iteria += f'客户等级:{customer_service_levels};'
                if sale_name != '':
                    query_iteria += f'销售:{sale_name};'
                if customer_source_default != '':
                    query_iteria += f'客户来源:{customer_source_default};'
                if query_iteria != '':
                    query_result_summary += f'查询条件：{query_iteria[:-1]}。'

                if len(resp) > display_number:
                    resp = resp[:display_number]
                query_crm_bus_customer_list = []
                for idx, item in enumerate(resp):
                    query_crm_bus_customer_list.append({
                        'no': idx + 1,
                        'customer_no': item['customerNo'],
                        'customer_name': item['customerName'],
                        'industry_line': item['industryLine'],
                        'business_type': item['businessType'],
                        'customer_role': item['customerRole'],
                        'customer_source': item['customerSource'],
                        'sale_name': item['saleName'],
                        'entry_status': item['entryStatus'],
                        'new_customer_importance': item['newCustomerImportance'],
                        'important_step': item['importantStep'],
                        'create_time': item['createTime'],
                        'integrity': item['integrity'],
                        "id": item['id']
                    })
                content = card_templates.crm_bus_customer_query_result(
                    template_variable={
                        "card_metadata": {
                            "card_name": "crm_bus_customer_delete",
                            "description": "展示报单查询结果"
                        },
                        'query_result_summary': query_result_summary,
                        "query_crm_bus_customer_list": query_crm_bus_customer_list,
                    }
                )
                return {
                    "success": "true",
                    "error_message": "",
                    "action": {
                        "action_name": "send_lark_form_card",
                        "card_name": "crm_bus_customer_query_result"
                    },
                    "data": {
                        "conv_id": conv_id,
                        "content": content

                    }
                }


        except Exception as e:
            logging.error("工具运行异常：", e)
            return repr(e)
