import logging

import requests
import json


def add_daily_or_weekly_report(report_type: str = "", report_time: str = "", work_summary: str = '', senders=None,
                               plans=None):
    # url = "https://nccemportal.yeepay.com/cem-api//workReportInfo/addWorkReportInfo"
    url = "http://nck8s.iaas.yp:30762/cem-api//workReportInfo/addWorkReportInfo"
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        # "pageType": "cemPortal",
        # "username": "liangliang.yan",
        # "Cookie": "JSESSIONID = CC1A0187CB8ABB474AA5D97614F21FC9",
        "Yuiassotoken": 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJsb2dpbl90eXBlIjoiQUNDT1VOVCIsIm1vYmlsZSI6IjE4NjExNzAwMzgwIiwibWlncmF0ZV91c2VyX2lkIjoiZWNkNTAyZDQtMmU2OC00NGI1LWEyNWYtZjIxZmQzM2IxNTIwIiwieC1pcCI6IjE3Mi4yNS4yNS4xMCIsInByaW5jaXBhbF9pZCI6IjE1MTAxIiwidG9rZW4iOiI4NzY1OGQ1Zi1mMTk1LTRmZTEtYjNiYS05Mzk1MTJlNjBhYjMiLCJsb2dpbl9uYW1lIjoibGlhbmdsaWFuZy55YW4iLCJ0d29fZmFjdG9yX3ZhbGlkIjp0cnVlLCJsb2dpbl90aW1lIjoiMjAyNC0wNC0yNSAyMDozNToyMCIsInNjb3BlIjoiIiwiY2FsbGJhY2siOiJodHRwczovL2RtYWxsLnllZXBheS5jb20vIy9kYXRhc2V0L2luZGV4Iiwic3NvdGlja2V0IjoiMjcyMWU0YTItNzFmZC00YzBjLWE2OWYtNTg2NGE2ZGNiYzA1IiwiZXhwIjoxNzE0MTM0OTIwLCJpYXQiOjE3MTQwNDY3MjAsImVtYWlsIjoibGlhbmdsaWFuZy55YW5AeWVlcGF5LmNvbSIsInVzZXJuYW1lIjoi5Lil5Lqu5LquIn0.8zOjyFI7JVKJ8-3KhU-1txvuVLfRP8WZZqbmfrGSoACfJ5oFP-XmDM9d3YvbS1k1Hf11GpIa_5NYUpIlnKyZJw'
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
