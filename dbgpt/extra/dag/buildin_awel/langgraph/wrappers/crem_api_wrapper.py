import requests
import json


def add_daily_or_weekly_report(report_type: str = "", report_time: str = "", work_summary: str = '', senders=None, plans=None):
    url = "https://nccemportal.yeepay.com/cem-api//workReportInfo/addWorkReportInfo"
    headers = {
        "Content-Type": "application/json",
        # "pageType": "cemPortal",
        # "username": "liangliang.yan",
        # "Cookie": "JSESSIONID = CC1A0187CB8ABB474AA5D97614F21FC9",
        "yuiassotoken": 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJsb2dpbl90eXBlIjoiQUNDT1VOVCIsIm1vYmlsZSI6IjEzMjgyNTEyODM2IiwibWlncmF0ZV91c2VyX2lkIjoiZTIyM2Q5M2QiLCJ4LWlwIjoiMTAuMTcxLjMuMjMwIiwicHJpbmNpcGFsX2lkIjoiMTc3ODkiLCJ0b2tlbiI6IjQ3YjEwNWI4LTE5NmQtNDFlOC05NGYzLWU3Y2Y4YmU2MWY3NSIsImxvZ2luX25hbWUiOiJjaGFvLmh1YW5nIiwidHdvX2ZhY3Rvcl92YWxpZCI6dHJ1ZSwibG9naW5fdGltZSI6IjIwMjQtMDQtMjUgMjA6MzA6MDEiLCJzY29wZSI6IiIsImNhbGxiYWNrIjoiaHR0cHM6Ly9uY2NlbXBvcnRhbC55ZWVwYXkuY29tLyMvY3JtL3dvcmtSZXBvcnQiLCJzc290aWNrZXQiOiJmY2VmYmY1ZS0yNzRkLTQ4NTYtYjY4Mi1lMDE2NDU2ZjRkZmIiLCJleHAiOjE3MTQxMzQ2MDEsImlhdCI6MTcxNDA0NjQwMSwiZW1haWwiOiJjaGFvLmh1YW5nQHllZXBheS5jb20iLCJ1c2VybmFtZSI6Ium7hOi2hSJ9.K_RM9yleCPhSNl8qszf8S0-lzgR0ftXDBSICASvu5BI_0qWWLR-9D9EVbjNh931jVBBZ_WtTBCuvrZD0X3GnTg'
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
        # "senders": senders if senders else "",
        "busPlanForTomorrowInfoList": [plans],
        "busWorkScheduleInfoList": [],
        "busAnnexInfos": []
    }

    response = requests.post(url, headers=headers, data=data)
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
