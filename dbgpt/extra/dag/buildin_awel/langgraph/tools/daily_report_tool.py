import logging
from typing import Optional, Type
from typing import List

from langchain.tools import BaseTool
from langchain_core.callbacks import (
    CallbackManagerForToolRun,
)
from pydantic import BaseModel, Field

from dbgpt.extra.dag.buildin_awel.lark import card_templates
from dbgpt.util.lark import larkutil


class DailyReportCollectInput(BaseModel):
    """

    """
    conv_id: str = Field(
        name="conv_id",
        description="the value of conv_id",
        default=""
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
        description="明日计划内容，可加多个，列表形式",
        default=[]
    )
    senders_name: str = Field(
        name="抄送人员",
        description="抄送人员，抄送给谁",
        default=""
    )


class DailyReportCollectTool(BaseTool):
    name: str = "daily_report_collect_tool"
    description: str = (
        "这是一个日报填写工具，帮助用户每天填写工作日报、每日工作总结。"
        "当需要填写日报时非常有用。 "
        "能够尽可能全的收集日报信息。"
        "调用本工具需要的参数值均来自用户的输入，可以默认为空，但是禁止随意编造。"
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
        print("开始运行日报填写工具：", conv_id, daily_report_content, create_date, daily_report_tomorrow_plans,
              senders_name)
        try:
            if daily_report_content == "":
                resp = {"success": "false", "response_message": "the description of daily_report_content"}
            elif create_date == "":
                resp = {"success": "false", "response_message": "the description of create_date"}
            else:
                resp = do_collect(
                    conv_id=conv_id,
                    daily_report_content=daily_report_content,
                    create_date=create_date,
                    daily_report_tomorrow_plans=daily_report_tomorrow_plans,
                    senders_name=senders_name
                )
            return resp
        except Exception as e:
            logging.error("工具运行异常：", e)
            return repr(e)


def do_collect(
        conv_id: str = "",
        daily_report_content: str = "",
        create_date: str = "",
        daily_report_tomorrow_plans: Optional[List[str]] = None,
        senders_name: str = ""
):
    """
    处理并收集日报信息，返回收集结果。
    """
    # 处理明日计划，如果为空则返回特定的消息
    if daily_report_tomorrow_plans is None:
        plans_description = "暂无明日计划"
    else:
        plans_description = ", ".join(daily_report_tomorrow_plans) if daily_report_tomorrow_plans else "明日计划列表为空"

    try:
        """
        我要填写日报：
        日报内容：今天完成了一次客户回访，进展正常。
        填写日期：2024-04-22
        明日计划：继续跟进
        """
        print("发送飞书日报卡片：", conv_id)
        larkutil.send_message(
            receive_id=conv_id,
            content=card_templates.create_daily_report_card_content(
                template_variable={
                    "card_metadata": {
                        "card_name": "daily_report_collect",
                        "description": "日报收集表单"
                    },
                    "daily_report_tomorrow_plans": plans_description,
                    "create_date": create_date,
                    "daily_report_content": daily_report_content,

                }
            ),
            receive_id_type="open_id",
            msg_type="interactive"
        )
    except Exception as e:
        logging.error("飞书日报卡片发送失败：", e)

    # 创建并返回结果字典
    return {
        "success": "true",
        "error_message": "",
        "data": {
            "next": "send_card_and_callback",
            "conv_id": conv_id,
            "daily_report_content": daily_report_content,
            "create_date": create_date,
            "daily_report_tomorrow_plans": plans_description,
            "senders_name": senders_name
        }
    }
