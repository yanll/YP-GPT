import logging

import requests
import json

from dbgpt.util import envutils


def add_daily_or_weekly_report(report_type: str = "", report_time: str = "", work_summary: str = '', senders=None,
                               plans=None):
    url = envutils.getenv("CREM_ENDPOINT") + "/workReportInfo/addWorkReportInfo"
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        # "pageType": "cemPortal",
        # "username": "liangliang.yan",
        # "Cookie": "JSESSIONID = CC1A0187CB8ABB474AA5D97614F21FC9",
        "Yuiassotoken": 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJsb2dpbl90eXBlIjoiQUNDT1VOVCIsIm1vYmlsZSI6IjE4NzU0MzE2MjQwIiwibWlncmF0ZV91c2VyX2lkIjoiZWM4Z2ExYWYiLCJ4LWlwIjoiMTcyLjI1LjI1LjEwIiwicHJpbmNpcGFsX2lkIjoiMTc3OTUiLCJ0b2tlbiI6IjQ5NmZjZjg3LTg2YTMtNDdiNS05NzU0LTJjNTQ3YTUxY2I4YyIsImxvZ2luX25hbWUiOiJodWF4dWUuemhhbmciLCJ0d29fZmFjdG9yX3ZhbGlkIjp0cnVlLCJsb2dpbl90aW1lIjoiMjAyNC0wNC0yOCAxODowOToxOCIsInNjb3BlIjoiIiwiY2FsbGJhY2siOiJodHRwczovL25jY2VtcG9ydGFsLnllZXBheS5jb20vIy9jcm0vZm9sbG93VmlzaXQiLCJzc290aWNrZXQiOiIyMGM4NDMyYS01N2M0LTRmMWEtYjY1Zi0wZjk3YjYwYzliOTMiLCJleHAiOjE3MTQzODUzNTgsImlhdCI6MTcxNDI5NzE1OCwiZW1haWwiOiJodWF4dWUuemhhbmdAeWVlcGF5LmNvbSIsInVzZXJuYW1lIjoi5byg5Y2O6ZuqIn0.0E0cvT9TPfE0tQl-l-BOnQMaFwb5zOklVWtfUFCymo_a-4W2qFMG1_2riGHRynLiuKi122UOgRYrQDSeNpHoLA'
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
