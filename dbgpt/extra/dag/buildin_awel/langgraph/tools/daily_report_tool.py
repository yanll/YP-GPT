import logging
from typing import List
from typing import Optional, Type

from langchain.tools import BaseTool
from langchain_core.callbacks import (
    CallbackManagerForToolRun,
)
from pydantic import BaseModel, Field


class DailyReportCollectInput(BaseModel):
    """
    我要填写日报：
    日报内容：今天完成了一次客户回访，进展正常。
    填写日期：2024-04-22
    明日计划：继续跟进
    """
    conv_id: str = Field(
        name="conv_id",
        description="the value of conv_id",
    )
    daily_report_content: str = Field(
        name="日报内容",
        description="日报内容",
        default=""
    )

    create_date: str = Field(
        name="日报填写日期",
        description="日报填写日期，格式：%Y-%m-%d",
        default=""
    )
    daily_report_tomorrow_plans: List[str] = Field(
        name="明日计划",
        description="明日计划内容",
        default=[]
    )
    senders_name: str = Field(
        name="抄送人员",
        description="抄送人员",
        default=""
    )


class DailyReportCollectTool(BaseTool):
    name: str = "daily_report_collect_tool"
    description: str = (
        "日报填写工具，辅助填写工作日报、每日工作总结。"
        "请注意：\n"
        "1、调用本工具需要的参数值来自用户输入，可以默认为空，但是禁止随意编造。\n"
        ""
    )
    args_schema: Type[BaseModel] = DailyReportCollectInput

    def _run(
            self,
            conv_id: str = "",
            daily_report_content: str = "",
            create_date: str = "",
            daily_report_tomorrow_plans: Optional[List[str]] = None,
            senders_name: str = "",
            run_manager: Optional[CallbackManagerForToolRun] = None,
    ):
        """Use the tool."""
        print("开始运行日报填写工具：", conv_id, daily_report_content)
        try:

            reuqires = []
            if daily_report_content == "":
                reuqires.append("daily_report_content")
            if create_date == "":
                reuqires.append("create_date")
            if len(reuqires) > 0:
                return {"success": "false", "response_message": "the description of " + "[" + ".".join(reuqires) + "]"}

            return handle(
                conv_id=conv_id,
                daily_report_content=daily_report_content,
                create_date=create_date,
                daily_report_tomorrow_plans=daily_report_tomorrow_plans
            )
        except Exception as e:
            logging.error("日报收集工具运行异常：" + conv_id + " " + daily_report_content, e)
            return repr(e)


def handle(
        conv_id: str = "",
        daily_report_content: str = "",
        create_date: str = "",
        daily_report_tomorrow_plans: Optional[List[str]] = None
):
    try:
        """
        处理并收集日报信息，返回收集结果。
        """
        # 处理明日计划，如果为空则返回特定的消息
        if daily_report_tomorrow_plans is None:
            plans_description = "暂无明日计划"
        else:
            plans_description = ", ".join(daily_report_tomorrow_plans) if daily_report_tomorrow_plans else "明日计划列表为空"

        return {
            "success": "true",
            "error_message": "",
            "action": {
                "action_name": "send_lark_form_card",
                "card_name": "daily_report_collect"
            },
            "data": {
                "conv_id": conv_id,
                "daily_report_tomorrow_plans": plans_description,
                "daily_report_content": daily_report_content,
                "create_date": create_date
            }
        }
    except Exception as e:
        raise Exception("日报数据组装失败：" + conv_id + " " + daily_report_content, e)
