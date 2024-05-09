import requests
from dbgpt.util import envutils
from dbgpt.util.lark import ssoutil
from dbgpt.extra.dag.buildin_awel.lark import card_templates

def daily_report_id_search(open_id, report_id):
    url = 'https://cem.yeepay.com/cem-api/workReportInfo/findWorkReportInfo'
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        'pageType': 'cemPortal',
        'yuiassotoken': ssoutil.get_sso_credential(open_id)
    }
    data = {
        "id": report_id
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        report_data = response.json()
        extracted_info_list = []

        if report_data and "data" in report_data and "list" in report_data["data"] and len(
                report_data["data"]["list"]) > 0:
            report = report_data["data"]["list"][0]
            extracted_info = {
                "createUser": report.get("createUser"),
                "senders": report.get("senders"),
                "createTime": report.get("createTime"),
                "workSummaryString": report.get("workSummaryString"),
                "busWorkScheduleInfoList": "",
                "busPlanForTomorrowInfoList": ""
            }

            today_work_str = ""
            for work_index, work in enumerate(report.get("busWorkScheduleInfoList", []), start=1):
                work_str = f"{work_index}.{work.get('workTitle')}, {work.get('workStatus')}"
                today_work_str += work_str + ", "
            extracted_info["busWorkScheduleInfoList"] = today_work_str.rstrip(", ")

            tomorrow_plan_str = ""
            for plan_index, plan in enumerate(report.get("busPlanForTomorrowInfoList", []), start=1):
                plan_str = f"{plan_index}.{plan.get('planContentString')}"
                tomorrow_plan_str += plan_str + ", "
            extracted_info["busPlanForTomorrowInfoList"] = tomorrow_plan_str.rstrip(", ")

            extracted_info_list.append(extracted_info)

        return extracted_info_list

    else:
        print(f"Request failed with status code: {response.status_code}")
        return []

# # 假设 report_id 是你要查询的日报的ID
# open_id = "your_open_id_here"
# report_id = "917edff51b35d0a8547c41019a97ecc1"
#
# # 获取并打印日报信息
# daily_report_info_list = daily_report_id_search(open_id, report_id)
# for daily_report_info in daily_report_info_list:
#     print(daily_report_info)
