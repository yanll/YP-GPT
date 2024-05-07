import logging

import requests
import json

from dbgpt.util import envutils


def add_daily_or_weekly_report(report_type: str = "", report_time: str = "", work_summary: str = '',
                               senders=None,
                               plans=None):
    url = envutils.getenv("CREM_ENDPOINT") + "/workReportInfo/addWorkReportInfo"
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "yuiassotoken": getssotoken()
    }

    # bus_plan_list = []
    # if plans:
    #     # 检查第一个元素的类型来决定如何处理整个列表
    #     if isinstance(plans[0], dict):
    #         # 周报的复杂结构处理
    #         for plan in plans:
    #             plan_dict = {
    #                 "planContentString": plan.get("planContentString", ""),
    #                 "customerNo": plan.get("customerNo", ""),
    #                 "customerName": plan.get("customerName", "")
    #             }
    #             bus_plan_list.append(plan_dict)
    #     else:
    #         # 日报的简单字符串列表处理
    #         for plan in plans:
    #             plan_dict = {"planContentString": plan}
    #             bus_plan_list.append(plan_dict)

    data = {
        "reportTitle": "",
        "reportType": report_type,
        "reportTime": report_time,
        "workSummaryString": work_summary,
        "busPlanForTomorrowInfoList": [],
        "busWorkScheduleInfoList": [],
        "busAnnexInfos": []
    }
    # ,
    # "senders": senders if senders else "",
    # "busPlanForTomorrowInfoList": [plans],
    # "busPlanForTomorrowInfoList": [],
    # "busWorkScheduleInfoList": [],
    # "busAnnexInfos": []
    print("提交日报到CREM：", data)
    response = requests.post(url, headers=headers, data=json.dumps(data))
    try:
        print(response.json())
    except Exception as e:
        print(response)
        logging.error("CREM日报调用失败：", e)
        raise e
    return response


def add_crm_bus_customer(customer_name: str = "",
                         industry_line: str = "",
                         customer_source: str = '',
                         customer_importance: str = ''):
    url = envutils.getenv("CREM_ENDPOINT") + "/crmCustomer/addCrmBusCustomer"
    headers = {
        "pagetype": "cemPortal",
        "Content-Type": "application/json; charset=utf-8",
        "yuiassotoken": getssotoken()
    }

    data = {
        "customer_name": customer_name,
        "industry_line": industry_line,
        "customer_source": customer_source,
        "customer_importance": customer_importance,
    }
    print("提交添加报单客户信息到CREM：", data)
    return {}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    try:
        print(response.json())
    except Exception as e:
        print(response)
        logging.error("CREM添加报单客户信息调用失败：", e)
        raise e
    return response

def getssotoken() -> str:
    return envutils.getenv("SSO_TOKEN")

# Example usage for daily and weekly reports
# 日报

# # 周报
# weekly_report_type = "周报"
# weekly_report_time = "2024-04-28 00:00:00"
# weekly_work_summary = "本周完成了项目A的设计，解决了项目B中的一些问题"
# weekly_senders = "张华雪"
# weekly_plans = [
#     {"planContentString": "下周继续完成项目A", "customerNo": "KA2024-A04220001", "customerName": "客户X"},
# ]
# weekly_result = add_report(weekly_report_type, weekly_report_time, weekly_work_summary, weekly_senders, weekly_plans)
# print("周报结果:", weekly_result)
