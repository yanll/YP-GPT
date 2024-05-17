import logging
from typing import Optional, Type

from langchain.tools import BaseTool
from langchain_core.callbacks import (
    CallbackManagerForToolRun
)
from pydantic import BaseModel, Field

from dbgpt.extra.dag.buildin_awel.langgraph.wrappers import crem_customer_search, crem_sales_board_dispaly, \
    crem_daily_push_messages
from dbgpt.util.lark import larkutil


class DailypushmessagetoolInput(BaseModel):
    conv_id: str = Field(
        name="conv_id",
        description="the value of conv_id",
    )

class Dailypushmessagetool(BaseTool):
    name: str = "daily_push_message_tool"
    description: str = (
        "每日推送信息查询工具。 "
        "请注意：\n"
        "1、调用本工具需要的参数值来自用户输入，可以默认为空，但是禁止随意编造。\n"
        ""
    )
    max_results: int = 20
    args_schema: Type[BaseModel] = DailypushmessagetoolInput

    def _run(
            self,
            conv_id: str = "",
            run_manager: Optional[CallbackManagerForToolRun] = None,
    ):
        """Use the tool."""
        print("开始执行每日推送信息查询工具：", conv_id,  self.max_results)
        try:
            resp_data = []
            if conv_id == "" :
                return {"success": "false", "response_message": "the description of conv_id"}
            data = crem_daily_push_messages.shujuqingk(
                open_id=conv_id
            )
            print("毛利详情", data)
            link = crem_sales_board_dispaly.mobile_process_data(
                open_id=conv_id
            )
            userinfo = larkutil.select_userinfo(
                open_id=conv_id)
            if userinfo and "name" in userinfo:
                nickname = userinfo["name"] + " "
                print("用户的姓名是", nickname)


            resp_data.append(data)
            sales_dispaly = link
            print("移动端的链接",sales_dispaly)
            query_str = (nickname).strip()
            print("推送人结果：", query_str, resp_data)
            list = []
            if resp_data and len(resp_data) == 0:
                return {"success": "true", "data": []}

            for m in resp_data:
                profit_yesterday = m.get("昨天的毛利", "")
                profit_day_before_yesterday = m.get("前天的毛利", "")
                yesterday_change_rate = m.get("昨天相对于前天的同比变化率", "")
                weekly_change_rate_formatted = m.get("上周同一时间的毛利变化率", "")
                profit_day7_before_yesterday = m.get("前7天的毛利总额", "")
                average_day7_before_yesterday= m.get("前7天的平均毛利", "")
                list.append({
                    "profit_yesterday": profit_yesterday if profit_yesterday is not None else "",
                    "profit_day_before_yesterday": profit_day_before_yesterday if profit_day_before_yesterday is not None else "",
                    "yesterday_change_rate": yesterday_change_rate if yesterday_change_rate is not None else "",
                    "weekly_change_rate_formatted": weekly_change_rate_formatted if weekly_change_rate_formatted is not None else "",
                    "profit_day7_before_yesterday": profit_day7_before_yesterday if profit_day7_before_yesterday is not None else "",
                    "average_day7_before_yesterday": average_day7_before_yesterday if average_day7_before_yesterday is not None else ""

                })

            return {
                "success": "true",
                "error_message": "",
                "action": {
                    "action_name": "send_lark_form_card",
                    "card_name": "daily_push_message_list_card"
                },
                "data": {
                    "list": list,
                    "query_str": query_str,
                    "sales_diapaly": sales_dispaly

                }
            }
        except Exception as e:
            logging.error("每日推送工具运行异常：", e)
            return repr(e)
