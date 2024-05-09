import logging
from typing import Optional, Type

from langchain.tools import BaseTool
from langchain_core.callbacks import (
    CallbackManagerForToolRun
)
from pydantic import BaseModel, Field

from dbgpt.extra.dag.buildin_awel.lark import card_templates
from dbgpt.util.lark import larkutil, lark_message_util
from dbgpt.extra.dag.buildin_awel.langgraph.wrappers import  crem_daily_report_search


class DailyReportSearchToolInput(BaseModel):
    conv_id: str = Field(
        name="conv_id",
        description="the value of conv_id",
    )
    sales_name: str = Field(name="销售名称", description="销售名称", default="")


class DailyReportSearchTool(BaseTool):
    name: str = "daily_report_search_tool"
    description: str = (
        "你是一个全面优化的日报信息查询工具，用于日报查询，结果准确、可信。 "
        "当你需要通过调用工具查询日报信息时非常有用。 "
        "输入参数应该是工具需要的全部参数。"
        "调用本工具需要的参数值均来自用户的输入，可以默认为空，但是禁止随意编造。"
        "请将查询结果数据整理并美化后输出。"
        "不要将日报查询工具跟日报填写工具混淆"
        "不要将日报查询工具与其他查询工具混淆"
    )
    max_results: int = 20
    args_schema: Type[BaseModel] = DailyReportSearchToolInput

    def _run(
            self,
            conv_id: str = "",
            sales_name: str = "",
            run_manager: Optional[CallbackManagerForToolRun] = None,
    ):
        """Use the tool."""
        print("开始执行日报信息查询工具：", conv_id, sales_name, self.max_results)
        try:
            resp_data = {}
            if sales_name == "":
                resp = {"success": "false", "response_message": "the description of  sales_name"}
            else:
                data = crem_daily_report_search.daily_report_search(
                    open_id=conv_id,
                    create_user=sales_name,

                )
                resp_data = data  # 直接从查询结果中获取data列表
            query_str = (sales_name + "" ).strip()
            print("日报查询结果：", query_str, resp_data)
            display_type = ""
            list = []
            if resp_data and len(resp_data) > 0:
                for m in resp_data:
                    reportTime = m.get("reportTime", "")
                    createUser = m.get("createUser", "")
                    senders = m.get("senders", "")
                    workSummaryString = m.get("workSummaryString", "")
                    id = m.get("id", "")
                    list.append({
                        "reportTime": reportTime if reportTime is not None else "",
                        "createUser": createUser if createUser is not None else "",
                        "senders": senders if senders is not None else "",
                        "workSummaryString": workSummaryString if workSummaryString is not None else "",
                        "id": id if id is not None else ""
                    })
                display_type = "form"
                lark_message_util.send_message(
                    receive_id=conv_id,
                    content=card_templates.search_daily_report_card_content(
                        template_variable={
                            "query_str": query_str,
                            "daily_report_list": list
                        }
                    ),
                    receive_id_type="open_id",
                    msg_type="interactive"
                )
            return {
                "success": "true",
                "error_message": "",
                "display_type": display_type,
                "data": list
            }
        except Exception as e:
            logging.error("日报查询工具运行异常：", e)
            return repr(e)
