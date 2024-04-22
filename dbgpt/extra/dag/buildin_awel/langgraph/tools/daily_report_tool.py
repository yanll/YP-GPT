from typing import Optional, Type

from langchain.tools import BaseTool
from langchain_core.callbacks import (
    CallbackManagerForToolRun,
)
from pydantic import BaseModel, Field

from dbgpt.util import larkutil


class DailyReportCollectInput(BaseModel):
    """

    """
    conv_id: str = Field(
        name="conv_id",
        description="value of conv_id",
        default=""
    )
    daily_report_content: str = Field(
        name="日报内容",
        description="日报内容",
        default=""
    )
    create_date: str = Field(
        name="",
        description="创建日期",
        default=""
    )


class DailyReportCollectTool(BaseTool):
    name: str = "daily_report_collect_tool"
    description: str = (
        "这是一个日报填写工具，帮助用户每天填写工作日报、每日工作总结。"
        "当需要填写日报时非常有用。 "
        "能够尽可能全的收集日报信息。"
        ""
    )
    args_schema: Type[BaseModel] = DailyReportCollectInput

    def _run(
            self,
            conv_id: str = "",
            daily_report_content: str = "",
            create_date: str = "",
            run_manager: Optional[CallbackManagerForToolRun] = None,
    ):
        """Use the tool."""
        print("开始运行日报填写工具：", conv_id, daily_report_content, create_date)
        try:
            if daily_report_content == "":
                resp = {"success": "false", "response_message": "the description of daily_report_content"}
            elif create_date == "":
                resp = {"success": "false", "response_message": "the description of create_date"}
            else:
                resp = do_collect(
                    daily_report_content=daily_report_content,
                    create_date=create_date
                )
            return resp
        except Exception as e:
            return repr(e)


def do_collect(
        daily_report_content: str = "",
        create_date: str = ""
):
    return {
        "success": "true",
        "error_message": "",
        "data": {
            "daily_report_content": daily_report_content,
            "create_date": create_date
        }
    }
