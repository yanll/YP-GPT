from typing import Optional, Type

from langchain.tools import BaseTool
from langchain_core.callbacks import (
    CallbackManagerForToolRun,
)
from pydantic import BaseModel, Field

from dbgpt.util import larkutil


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
    visit_content: str = Field(
        name="拜访内容",
        description="拜访内容",
        default=""
    )
    visit_address: str = Field(
        name="拜访地址",
        description="拜访地址",
        default=""
    )
    visit_date: str = Field(
        name="拜访日期",
        description="拜访日期",
        default=""
    )


class CustomerVisitRecordCollectTool(BaseTool):
    name: str = "customer_visit_record_collect_tool"
    description: str = (
        "这是一个客户拜访记录填写工具，帮助用户填写客户拜访记录、客户拜访信息总结。"
        "当需要填写客户拜访记录时非常有用。 "
        "能够尽可能全的收集拜访记录信息。"
        ""
    )
    args_schema: Type[BaseModel] = CustomerVisitRecordCollectInput

    def _run(
            self,
            conv_id: str = "",
            customer_name: str = "",
            visit_content: str = "",
            visit_address: str = "",
            visit_date: str = "",
            run_manager: Optional[CallbackManagerForToolRun] = None,
    ):
        """Use the tool."""
        print("开始运行客户拜访填写工具：", conv_id, customer_name, visit_content, visit_address, visit_date)
        try:
            if customer_name == "":
                resp = {"success": "false", "response_message": "the description of customer_name"}
            elif visit_content == "":
                resp = {"success": "false", "response_message": "the description of visit_content"}
            elif visit_address == "":
                resp = {"success": "false", "response_message": "the description of visit_address"}
            elif visit_date == "":
                resp = {"success": "false", "response_message": "the description of visit_date"}
            else:
                resp = do_collect(
                    customer_name=customer_name,
                    visit_content=visit_content,
                    visit_address=visit_address,
                    visit_date=visit_date
                )
            return resp
        except Exception as e:
            return repr(e)


def do_collect(
        customer_name: str = "",
        visit_content: str = "",
        visit_address: str = "",
        visit_date: str = ""
):
    return {
        "success": "true",
        "error_message": "",
        "data": {
            "customer_name": customer_name,
            "visit_content": visit_content,
            "visit_address": visit_address,
            "visit_date": visit_date
        }
    }
