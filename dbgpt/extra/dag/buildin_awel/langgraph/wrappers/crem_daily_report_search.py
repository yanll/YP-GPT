import json
import logging

import requests

from dbgpt.util import envutils
from dbgpt.util.lark import ssoutil

def daily_report_search(create_user):
    url = envutils.getenv("CREM_ENDPOINT") +'/workReportInfo/findWorkReportInfo'

    headers = {
        "Content-Type": "application/json; charset=utf-8",
        'pageType': 'cemPortal',
        "yuiassotoken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJsb2dpbl90eXBlIjoiQUNDT1VOVCIsIm1vYmlsZSI6IjE4NzU0MzE2MjQwIiwibWlncmF0ZV91c2VyX2lkIjoiZWM4Z2ExYWYiLCJ4LWlwIjoiMTcyLjI1LjI1LjEwIiwicHJpbmNpcGFsX2lkIjoiMTc3OTUiLCJ0b2tlbiI6ImJlYmI5Yjg2LTMzMGUtNGY3MC05ZTg5LTRjNTJlNmZmYjQ2NyIsImxvZ2luX25hbWUiOiJodWF4dWUuemhhbmciLCJ0d29fZmFjdG9yX3ZhbGlkIjp0cnVlLCJsb2dpbl90aW1lIjoiMjAyNC0wNS0wOCAwOTo1ODoxNCIsInNjb3BlIjoiIiwiY2FsbGJhY2siOiJodHRwczovL25jY2VtcG9ydGFsLnllZXBheS5jb20vIy9jdXN0b21lci9jdXN0b21lclNlYXJjaCIsInNzb3RpY2tldCI6IjhkMjJhYmMwLTNlMDAtNDczNi1iMWM5LWFlZDVjM2VhYzJlZSIsImV4cCI6MTcxNTIxOTg5NCwiaWF0IjoxNzE1MTMxNjk0LCJlbWFpbCI6Imh1YXh1ZS56aGFuZ0B5ZWVwYXkuY29tIiwidXNlcm5hbWUiOiLlvKDljY7pm6oifQ.JkoSEqraFBRf4eUuzp8oqeEUPkQEHA-RCJoFQy7XblhJyPn14wFMZJBg5ZwYVYevTkNFdDL8lrAOAGtL77iQLg"
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
            'createUser': report.get('createUser', ''),
            'senders': report.get('senders', ''),
            'reportTime': report.get('reportTime', ''),
            'workSummaryString': report.get('workSummaryString', ''),
            'id': report.get('id', '')
        }
        extracted_data.append(report_data)
    return extracted_data


# 使用示例
# results = daily_report_search("张华雪")
# for result in results:
#     print(result)