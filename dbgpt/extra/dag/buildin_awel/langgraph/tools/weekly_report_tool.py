import logging
from typing import Optional, Type
from typing import List
from langchain.tools import BaseTool
from langchain_core.callbacks import (
    CallbackManagerForToolRun,
)
from pydantic import BaseModel, Field

from dbgpt.util import larkutil


class PlanDetail(BaseModel):
    plan_content: str = Field(
        name="下周计划内容",
        description="下周计划内容（从输入的信息中提取，默认为空，不要编造）",
        default=""
    )


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
        description="周报内容（从输入的信息中提取，默认为空，不要编造）",
        default=""
    )
    create_date: str = Field(
        name="创建日期",
        description="创建日期，格式：%Y-%m-%d（从输入的信息中提取，默认为空，不要编造）",
        default=""
    )
    weekly_report_next_week_plans: List[PlanDetail] = Field(
        name="下周计划内容",
        description="下周计划内容（从输入的信息中提取，默认为空，不要编造）",
        default=[]
    )

    senders_name: str = Field(
        name="抄送人员",
        description="抄送给谁（从输入的信息中提取，默认为空，不要编造）",
        default=""
    )


class WeeklyReportCollectTool(BaseTool):
    name: str = "weekly_report_collect_tool"
    description: str = (
        "这是一个周报填写工具，帮助用户填写工作周报、填写每周工作总结。"
        "当需要填写周报/写周报/总结周报时非常有用。 "
        "能够尽可能全的收集周报信息。"
        ""
    )
    args_schema: Type[BaseModel] = WeeklyReportCollectInput

    def _run(self,
             conv_id: str,
             weekly_report_content: str,
             create_date: str,
             run_manager: Optional[CallbackManagerForToolRun] = None,
             senders_name: Optional[str] = "",
             weekly_report_next_week_plans: Optional[List[PlanDetail]] = None):

        """Use the tool.77"""
        print("开始运行周报填写工具：", conv_id, weekly_report_content, create_date, senders_name,
              weekly_report_next_week_plans)
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
            logging.error("工具运行异常：", e)
            return repr(e)


def do_collect(
        weekly_report_content: str = "",
        create_date: str = "",
        weekly_report_next_week_plans: Optional[List[str]] = None,
        senders_name: str = ""
):
    """
        处理并收集日报信息，返回收集结果。
        """
    # 处理明日计划，如果为空则返回特定的消息
    if weekly_report_next_week_plans is None:
        plans_description = ""
    else:
        plans_description = ", ".join(weekly_report_next_week_plans) if weekly_report_next_week_plans else ""

    # 创建并返回结果字典
    return {
        "success": "true",
        "error_message": "",
        "data": {
            "daily_report_content": weekly_report_content,
            "create_date": create_date,
            "weekly_report_next_week_plans": plans_description,
            "senders_name": senders_name
        }
    }
