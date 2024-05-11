import logging
from typing import Optional, Type

from langchain.tools import BaseTool
from langchain_core.callbacks import (
    CallbackManagerForToolRun,
)
from pydantic import BaseModel, Field

from dbgpt.util.lark import lark_card_util


class CustomerVisitRecordCollectInput(BaseModel):
    """
    我要填写客户拜访跟进记录：

       - 客户名称：YP-GPT报单客户测试
       - 拜访形式：电话/微信拜访
       - 拜访类型：初次拜访
       - 拜访内容：测试拜访情况
       - 拜访日期：2024年5月2日
       - 联系人：张先生



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
    visit_method: str = Field(
        name="拜访形式",
        description="拜访形式，" +
                    lark_card_util.card_options_to_input_field_description(
                        lark_card_util.card_options_for_visit_methods()
                    ),
        default=""
    )
    visit_type: str = Field(
        name="拜访类型",
        description="拜访类型" +
                    lark_card_util.card_options_to_input_field_description(
                        lark_card_util.card_options_for_visit_types()
                    ),
        default=""
    )
    visit_content: str = Field(
        name="拜访内容",
        description="拜访内容",
        default=""
    )
    visit_date: str = Field(
        name="拜访日期",
        description="拜访日期",
        default=""
    )
    contacts: str = Field(
        name="联系人",
        description="联系人",
        default=""
    )


class CustomerVisitRecordCollectTool(BaseTool):
    name: str = "customer_visit_record_collect_tool"
    description: str = (
        "这是一个客户拜访记录填写工具，帮助用户填写客户拜访记录、客户拜访信息总结。"
        "当需要填写客户拜访记录时非常有用。 "
        "能够尽可能全的收集拜访记录信息。"
        "调用本工具需要的参数值均来自用户的输入，可以默认为空，但是禁止随意编造。"
        ""
    )
    args_schema: Type[BaseModel] = CustomerVisitRecordCollectInput

    def _run(
            self,
            conv_id: str = "",
            customer_name: str = "",
            visit_method: str = "",
            visit_type: str = "",
            visit_content: str = "",
            visit_date: str = "",
            contacts: str = "",
            run_manager: Optional[CallbackManagerForToolRun] = None,
    ):
        """Use the tool."""
        print("开始运行客户拜访填写工具：", conv_id, customer_name, visit_method, visit_type, visit_content, visit_date,
              contacts)
        try:
            reuqires = []
            if customer_name == "":
                reuqires.append("customer_name")
            if visit_method == "":
                reuqires.append("visit_method")
            if visit_type == "":
                reuqires.append("visit_type")
            if visit_content == "":
                reuqires.append("visit_content")
            if visit_date == "":
                reuqires.append("visit_date")
            if contacts == "":
                reuqires.append("contacts")
            if len(reuqires) > 0:
                return {"success": "false", "response_message": "the description of " + str(reuqires)}

            return handle(
                conv_id=conv_id,
                customer_name=customer_name,
                visit_method=visit_method,
                visit_type=visit_type,
                visit_content=visit_content,
                visit_date=visit_date,
                contacts=contacts
            )
        except Exception as e:
            logging.error("跟进拜访工具运行异常：" + conv_id + " " + visit_content, e)
            return repr(e)


def handle(
        conv_id: str,
        customer_name: str = "",
        visit_method: str = "",
        visit_type: str = "",
        visit_content: str = "",
        visit_date: str = "",
        contacts: str = ""
):
    try:
        return {
            "success": "true",
            "error_message": "",
            "action": {
                "action_name": "send_lark_form_card",
                "card_name": "customer_visit_record_collect"
            },
            "data": {
                "conv_id": conv_id,
                "customer_name": customer_name,
                "visit_content": visit_content,
                "contacts": contacts,
                "visit_date": visit_date,
                "visit_method": lark_card_util.get_action_index_by_text_from_options(
                    visit_method,
                    lark_card_util.card_options_for_visit_methods()
                ),
                "visit_methods": lark_card_util.card_options_for_visit_methods(),
                "visit_type": lark_card_util.get_action_index_by_text_from_options(
                    visit_type,
                    lark_card_util.card_options_for_visit_types()
                ),
                "visit_types": lark_card_util.card_options_for_visit_types()
            }
        }
    except Exception as e:
        raise Exception("跟进拜访数据组装失败：" + conv_id + " " + visit_content, e)
