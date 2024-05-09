import json

from dbgpt.extra.dag.buildin_awel.langgraph.wrappers.crem_daily_report_id_search import daily_report_id_search
from dbgpt.extra.dag.buildin_awel.lark import card_templates
from dbgpt.util.lark import larkutil
import logging

def card_send_daily_report_search(open_id,report_id,report_time,conv_id):

    try:
        if report_id == "":
            # 日报ID为空，返回错误消息
            return {"success": False, "response_message": "日报ID不能为空"}

        # 调用外部函数获取商户信息分析结果
        else:
            #report_id = "917edff51b35d0a8547c41019a97ecc1"
            daily_report_analysis = daily_report_id_search(open_id,report_id)
            print("完整返回结果", daily_report_analysis)
            extracted_info = daily_report_analysis
            print("日报返回结果",extracted_info)

            resp_data = {}
            resp_data = extracted_info

        query_str = (report_time + "" ).strip()
        print("日报详情查询结果：", query_str, resp_data)
        display_type = ""
        list = []
        if resp_data and len(resp_data) > 0:
            for m in resp_data:
                createTime = m.get("createTime", "")
                createUser = m.get("createUser", "")
                senders = m.get("senders", "")
                busWorkScheduleInfoList = m.get("busWorkScheduleInfoList", "")
                workSummaryString = m.get("workSummaryString", "")
                busPlanForTomorrowInfoList = m.get("busPlanForTomorrowInfoList", "")
                list.append({
                    "createUser": createUser if createUser is not None else "",
                    "createTime": createTime if createTime is not None else "",
                    "senders": senders if senders is not None else "",
                    "busWorkScheduleInfoList": busWorkScheduleInfoList if busWorkScheduleInfoList is not None else "",
                    "workSummaryString": workSummaryString if workSummaryString is not None else "",
                    "busPlanForTomorrowInfoList": busPlanForTomorrowInfoList if busPlanForTomorrowInfoList is not None else ""
                })
            display_type = "form"
            larkutil.send_message(
                receive_id=conv_id,
                content=card_templates.search_daily_report_id_card_content(
                    template_variable={
                        "query_str": query_str,
                        "daily_report_id_list": list
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

