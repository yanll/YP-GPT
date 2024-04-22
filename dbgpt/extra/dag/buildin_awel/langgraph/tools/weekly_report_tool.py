from typing import Optional, Type

from langchain.tools import BaseTool
from langchain_core.callbacks import (
    CallbackManagerForToolRun,
)
from pydantic import BaseModel, Field

from dbgpt.util import larkutil


class WeeklyReportCollectInput(BaseModel):
    """

    """
    conv_id: str = Field(
        name="conv_id",
        description="value of conv_id",
        default=""
    )
    weekly_report_content: str = Field(
        name="周报内容",
        description="日报内容",
        default=""
    )
    create_date: str = Field(
        name="",
        description="创建日期",
        default=""
    )


class WeeklyReportCollectTool(BaseTool):
    name: str = "weekly_report_collect_tool"
    description: str = (
        "这是一个周报填写工具，帮助用户每周填写工作周报、每周工作总结。"
        "当需要填写周报时非常有用。 "
        "能够尽可能全的收集周报信息。"
        ""
    )
    args_schema: Type[BaseModel] = WeeklyReportCollectInput

    def _run(
            self,
            conv_id: str = "",
            weekly_report_content: str = "",
            create_date: str = "",
            run_manager: Optional[CallbackManagerForToolRun] = None,
    ):
        """Use the tool."""
        print("开始运行日报填写工具：", conv_id, weekly_report_content, create_date)
        try:
            if weekly_report_content == "":
                resp = {"success": "false", "response_message": "the description of weekly_report_content"}
            elif create_date == "":
                resp = {"success": "false", "response_message": "the description of create_date"}
            else:
                resp = do_collect(
                    weekly_report_content=weekly_report_content,
                    create_date=create_date
                )
            return resp
        except Exception as e:
            return repr(e)


def do_collect(
        weekly_report_content: str = "",
        create_date: str = ""
):
    return {
        "success": "true",
        "error_message": "",
        "data": {
            "weekly_report_content": weekly_report_content,
            "create_date": create_date
        }
    }
