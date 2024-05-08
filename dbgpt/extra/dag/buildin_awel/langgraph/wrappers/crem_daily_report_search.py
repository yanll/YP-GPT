import json
import logging

import requests

from dbgpt.util import envutils
from dbgpt.util.lark import ssoutil

def daily_report_search(open_id,create_user):
    url = envutils.getenv("CREM_ENDPOINT") +'/workReportInfo/findWorkReportInfo'

    headers = {
        "Content-Type": "application/json; charset=utf-8",
        'pageType': 'cemPortal',
        'yuiassotoken': ssoutil.get_sso_credential(open_id)
    }

    data = {
        "reportType": "",
        "operateType": "",
        "workSummaryString": "",
        "createUser": create_user,
        "pageSize": 5,
        "pageNum": 1
    }

    response = requests.post(url, headers=headers, json=data)
    response_json = response.json()

    # 数据提取
    report_list = response_json.get('data', {}).get('list', [])
    extracted_data = []
    for report in report_list:
        report_data = {
            'reportTime': report.get('reportTime', ''),
            'createUser': report.get('createUser', ''),
            'senders': report.get('senders', ''),
            'workSummaryString': report.get('workSummaryString', ''),
            'id': report.get('id', '')
        }
        extracted_data.append(report_data)
    return extracted_data


# # 使用示例
# results = daily_report_search("张华雪")
# for result in results:
#     print(result)