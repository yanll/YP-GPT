import logging
from typing import Optional, Type

from langchain.tools import BaseTool
from langchain_core.callbacks import (
    CallbackManagerForToolRun,
)
from pydantic import BaseModel, Field

from dbgpt.extra.dag.buildin_awel.lark import card_templates
from dbgpt.util.lark import larkutil


class CustomerVisitRecordCollectInput(BaseModel):
    """

    """
    conv_id: str = Field(
        name="conv_id",
        description="value of conv_id",
        default=""
    )
    customer_name: str = Field(
        name="客户名称",
        description="客户名称",
        default=""
    )
    visit_method: str = Field(
        name="拜访形式",
        description="拜访形式",
        default=""
    )
    visit_type: str = Field(
        name="拜访类型",
        description="拜访类型",
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
            if customer_name == "":
                resp = {"success": "false", "response_message": "the description of customer_name"}
            elif visit_method == "":
                resp = {"success": "false", "response_message": "the description of visit_method"}
            elif visit_type == "":
                resp = {"success": "false", "response_message": "the description of visit_type"}
            elif visit_content == "":
                resp = {"success": "false", "response_message": "the description of visit_content"}
            elif visit_date == "":
                resp = {"success": "false", "response_message": "the description of visit_date"}
            elif contacts == "":
                resp = {"success": "false", "response_message": "the description of contacts"}
            else:
                resp = do_collect(
                    conv_id=conv_id,
                    customer_name=customer_name,
                    visit_method=visit_method,
                    visit_type=visit_type,
                    visit_content=visit_content,
                    visit_date=visit_date,
                    contacts=contacts
                )
            return resp
        except Exception as e:
            logging.error("工具运行异常：", e)
            return repr(e)


def do_collect(
        conv_id: str,
        customer_name: str = "",
        visit_method: str = "",
        visit_type: str = "",
        visit_content: str = "",
        visit_date: str = "",
        contacts: str = ""
):
    try:
        """
        我要填写客户拜访跟进记录：

       - 客户名称：张华雪报单客户测试
       - 拜访形式：电话/微信拜访
       - 拜访类型：初次拜访
       - 拜访内容：测试拜访情况
       - 拜访日期：2024年5月2日
       - 联系人  ：张先生



        """
        print("发送飞书拜访卡片：", conv_id)
        larkutil.send_message(
            receive_id=conv_id,
            content=card_templates.create_customer_visit_record_card_content(
                template_variable={
                    "card_metadata": {
                        "card_name": "customer_visit_record_collect",
                        "description": "拜访收集表单"
                    },
                    "customer_name": customer_name,
                    "visit_content": visit_content,
                    "contacts": contacts

                }
            ),
            receive_id_type="open_id",
            msg_type="interactive"
        )
    except Exception as e:
        logging.error("飞书拜访跟进卡片发送失败：", e)

    return {
        "success": "true",
        "error_message": "",
        "data": {
            "conv_id": conv_id,
            "customer_name": customer_name,
            "visit_method": visit_method,
            "visit_type": visit_type,
            "visit_content": visit_content,
            "visit_date": visit_date,
            "contacts": contacts
        }
    }
