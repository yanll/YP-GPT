import requests
import json


def add_daily_report(report_type, report_time, work_summary, senders=None, plans=None):
    url = "https://nccemportal.yeepay.com/cem-api//workReportInfo/addWorkReportInfo"
    headers = {
        "Content-Type": "application/json",
        "pageType": "cemPortal",
        "username": "liangliang.yan",
        # "yuiassotoken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJsb2dpbl90eXBlIjoiQUNDT1VOVCIsIm1vYmlsZSI6IjE4NzU0MzE2MjQwIiwibWlncmF0ZV91c2VyX2lkIjoiZWM4Z2ExYWYiLCJ4LWlwIjoiMTcyLjI1LjI1LjEwIiwicHJpbmNpcGFsX2lkIjoiMTc3OTUiLCJ0b2tlbiI6ImYzNjViYzczLWQ0ZTItNGJmMi04ODQ3LTVhYjQxZTcyMmI0MyIsImxvZ2luX25hbWUiOiJodWF4dWUuemhhbmciLCJ0d29fZmFjdG9yX3ZhbGlkIjp0cnVlLCJsb2dpbl90aW1lIjoiMjAyNC0wNC0yMiAxNDo0Mjo0MiIsInNjb3BlIjoiIiwiY2FsbGJhY2siOiJodHRwOi8veWNlbmMueWVlcGF5LmNvbTozMDg5OS9sb2dpbi8_dHM9Iiwic3NvdGlja2V0IjoiNDg3ZGU5NmMtZGJjYy00MWZjLTgyMzItNzNjZWJhNTQ0ZjEzIiwiZXhwIjoxNzEzODU0NTYyLCJpYXQiOjE3MTM3NjYzNjIsImVtYWlsIjoiaHVheHVlLnpoYW5nQHllZXBheS5jb20iLCJ1c2VybmFtZSI6IuW8oOWNjumbqiJ9.AThudhIZo8nUu_u_-WT9XT52liVdKPeWx_cHVMt29QvpoG7GMF_3G_pM5xNNmz_wc_4E0b78o8xf7Q22gnwbaw",
    }

    bus_plan_list = []
    if plans:
        # 检查第一个元素的类型来决定如何处理整个列表
        if isinstance(plans[0], dict):
            # 周报的复杂结构处理
            for plan in plans:
                plan_dict = {
                    "planContentString": plan.get("planContentString", ""),
                    "customerNo": plan.get("customerNo", ""),
                    "customerName": plan.get("customerName", "")
                }
                bus_plan_list.append(plan_dict)
        else:
            # 日报的简单字符串列表处理
            for plan in plans:
                plan_dict = {"planContentString": plan}
                bus_plan_list.append(plan_dict)

    data = {
        "reportTitle": "",
        "reportType": report_type,
        "reportTime": report_time,
        "workSummaryString": work_summary,
        "senders": senders if senders else "",
        "busPlanForTomorrowInfoList": bus_plan_list,
        "busWorkScheduleInfoList": [],
        "busAnnexInfos": []
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()


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
