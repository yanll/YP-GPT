import logging
from typing import Optional, Type

from langchain.tools import BaseTool
from langchain_core.callbacks import (
    CallbackManagerForToolRun
)
from pydantic import BaseModel, Field

from dbgpt.extra.dag.buildin_awel.langgraph.wrappers import crem_sales_board_dispaly, \
    crem_daily_push_messages, authority_Industryline_user
from dbgpt.util.lark import larkutil
import datetime

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
        global value_colour_yesterday_change_rate, value_colour_weekly_change_rate
        print("开始执行每日推送信息查询工具：", conv_id, self.max_results)
        try:
            resp_data = []
            if conv_id == "":
                return {"success": "false", "response_message": "the description of conv_id"}
            data = crem_daily_push_messages.shujuqingk(
                open_id=conv_id
            )
            print("毛利详情", data)


            yesterday_change_rate = data.get("昨天相对于前天的同比变化率", "")
            weekly_change_rate_formatted = data.get("上周同一时间的毛利变化率", "")
            yesterday777_change_rate_formatted = data.get("昨日同比7日平均变化率", "")

            # 颜色判断和富文本信息生成
            numeric_change_rate_yesterday = float(yesterday_change_rate.strip('%'))
            numeric_change_rate_weekly = float(weekly_change_rate_formatted.strip('%'))
            numeric_change_rate_yesterday777 = float(yesterday777_change_rate_formatted.strip('%'))

            colour_yesterday_change_rate = "green" if numeric_change_rate_yesterday > 0 else "red"
            up_and_down_yesterday = "↑" if colour_yesterday_change_rate == "green" else "↓"
            value_colour_yesterday_change_rate = f"<text_tag color={colour_yesterday_change_rate}>{yesterday_change_rate}{up_and_down_yesterday}</text_tag>"

            colour_weekly_change_rate = "green" if numeric_change_rate_weekly > 0 else "red"
            up_and_down_weekly = "↑" if colour_weekly_change_rate == "green" else "↓"
            value_colour_weekly_change_rate = f"<text_tag color={colour_weekly_change_rate}>{weekly_change_rate_formatted}{up_and_down_weekly}</text_tag>"

            colour_yesterday777_change_rate = "green" if numeric_change_rate_yesterday777 > 0 else "red"
            up_and_down_yesterday = "↑" if colour_yesterday777_change_rate == "green" else "↓"
            value_colour_yesterday777_change_rate = f"<text_tag color={colour_yesterday777_change_rate}>{yesterday777_change_rate_formatted}{up_and_down_yesterday}</text_tag>"

            print("昨日的颜色", value_colour_yesterday_change_rate)
            print("上周的颜色", value_colour_weekly_change_rate)

            link = crem_sales_board_dispaly.mobile_process_data(
                open_id=conv_id
            )
            userinfo = larkutil.select_userinfo(
                open_id=conv_id)
            if userinfo and "name" in userinfo:
                nickname = str(userinfo["name"])
                print("用户的姓名是", nickname)

            resp_data.append(data)
            sales_dispaly = link
            print("移动端的链接", sales_dispaly)
            query_str = (nickname).strip()
            print("推送人结果：", query_str, resp_data)


            user_type_value = authority_Industryline_user.sales_board_display(open_id=conv_id)
            print("人员权限为", user_type_value)

            # 如果 query_str 是 "高峰" 或 "黄伟-1"，则将 user_type_value 设置为 0
            if query_str in ["高峰", "黄伟-1"]:
                user_type_value = 0

            if user_type_value == 0:
                user_type = "0"
            elif user_type_value == 1:
                user_type = "1"
            elif user_type_value == 2:
                user_type = "2"
            else:
                user_type = "0"
            print(user_type)

            # 根据user_type_value的值进行判断，并转换成对应的文字描述
            if user_type_value == 0:
                user_type_description = "您与名下销售毛利总和"
            elif user_type_value == 1:
                user_type_description = "您的毛利"
            elif user_type_value == 2:
                user_type_description = "您与名下销售毛利总和"
            else:
                user_type_description = "未知的权限类型"

            # 输出对应的文字描述
            print(user_type_description)
            # industry_line = authority_Industryline_user.industry_line(
            #     open_id=conv_id
            # )
            # print("人员行业线为",industry_line)

            current_date = datetime.date.today()
            # 将日期格式化为“您06月03日（周一）”的形式
            formatted_date = current_date.strftime("%m月%d日（周") + ["一", "二", "三", "四", "五", "六", "日"][
                current_date.weekday()] + "）"
            print("当前日期:", formatted_date)

            list = []
            if resp_data and len(resp_data) == 0:
                return {"success": "true", "data": []}

            for m in resp_data:
                profit_yesterday = m.get("昨天的毛利", "")
                profit_day_before_yesterday = m.get("前天的毛利", "")
                yesterday_change_rate = m.get("昨天相对于前天的同比变化率", "")
                weekly_change_rate_formatted = m.get("上周同一时间的毛利变化率", "")
                profit_day7_before_yesterday = m.get("前7天的毛利总额", "")
                average_day7_before_yesterday = m.get("前7天的平均毛利", "")
                yesterday777_change_rate_formatted = m.get("昨日同比7日平均变化率", "")


                list.append({
                    "profit_yesterday": profit_yesterday if profit_yesterday is not None else "",
                    "profit_day_before_yesterday": profit_day_before_yesterday if profit_day_before_yesterday is not None else "",
                    "yesterday_change_rate": yesterday_change_rate if yesterday_change_rate is not None else "",
                    "weekly_change_rate_formatted": weekly_change_rate_formatted if weekly_change_rate_formatted is not None else "",
                    "profit_day7_before_yesterday": profit_day7_before_yesterday if profit_day7_before_yesterday is not None else "",
                    "average_day7_before_yesterday": average_day7_before_yesterday if average_day7_before_yesterday is not None else "",
                    "yesterday777_change_rate_formatted": yesterday777_change_rate_formatted if yesterday777_change_rate_formatted is not None else "",

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
                    "user_type_value": user_type,
                    "user_type_description": user_type_description,
                    "sales_diapaly": sales_dispaly,
                    "formatted_date": formatted_date,

                    "value_colour_yesterday_change_rate": value_colour_yesterday_change_rate,
                    "value_colour_weekly_change_rate": value_colour_weekly_change_rate,
                    "value_colour_yesterday777_change_rate": value_colour_yesterday777_change_rate

                }
            }
        except Exception as e:
            logging.error("每日推送工具运行异常：", e)
            return repr(e)
