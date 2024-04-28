import requests
import json

from dbgpt.util import envutils


#

def add_customer_visit_record(customer_name, followUpText, followUpTime, followUpTypeName, visitTypeName, contacts):
    url = envutils.getenv("CREM_ENDPOINT")+'/busFollowUp/addCreateFollowUp'

    headers = {
        'Yuiassotoken': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJsb2dpbl90eXBlIjoiQUNDT1VOVCIsIm1vYmlsZSI6IjE4NzU0MzE2MjQwIiwibWlncmF0ZV91c2VyX2lkIjoiZWM4Z2ExYWYiLCJ4LWlwIjoiMTcyLjI1LjI1LjEwIiwicHJpbmNpcGFsX2lkIjoiMTc3OTUiLCJ0b2tlbiI6IjQ5NmZjZjg3LTg2YTMtNDdiNS05NzU0LTJjNTQ3YTUxY2I4YyIsImxvZ2luX25hbWUiOiJodWF4dWUuemhhbmciLCJ0d29fZmFjdG9yX3ZhbGlkIjp0cnVlLCJsb2dpbl90aW1lIjoiMjAyNC0wNC0yOCAxODowOToxOCIsInNjb3BlIjoiIiwiY2FsbGJhY2siOiJodHRwczovL25jY2VtcG9ydGFsLnllZXBheS5jb20vIy9jcm0vZm9sbG93VmlzaXQiLCJzc290aWNrZXQiOiIyMGM4NDMyYS01N2M0LTRmMWEtYjY1Zi0wZjk3YjYwYzliOTMiLCJleHAiOjE3MTQzODUzNTgsImlhdCI6MTcxNDI5NzE1OCwiZW1haWwiOiJodWF4dWUuemhhbmdAeWVlcGF5LmNvbSIsInVzZXJuYW1lIjoi5byg5Y2O6ZuqIn0.0E0cvT9TPfE0tQl-l-BOnQMaFwb5zOklVWtfUFCymo_a-4W2qFMG1_2riGHRynLiuKi122UOgRYrQDSeNpHoLA',
        'Content-Type': 'application/json',
        'Cookie': 'JSESSIONID=2F457B72BE5AF9189C4492286D407C20'
    }

    data = {
        "customerName": customer_name,
        "customerNo": "KA2024-A04260006",
        "followUpText": followUpText,
        "followUpTime": followUpTime,
        "followUpTypeName": followUpTypeName,
        "visitTypeName": "",
        "type": 1,
        "headEntityKey": "followUpInfo",
        "contactIdList": ["0a527c79f2ad770f1b880b8209b2223f"],
        "contacts": contacts
    }

    response = requests.post(url, headers=headers, json=data)

    return response.text


if __name__ == "__main__":
    # 从外部传入参数调用函数
    customerName = "YP-gpt报单客户测试"
    followUpText = "测试24"
    followUpTime = "2024-04-26 14:36:57"
    followUpTypeName = "在外约谈"
    visitTypeName = "签约后日常拜访"
    contacts = "张先生"

    response_text = add_customer_visit_record(customerName, followUpText, followUpTime, followUpTypeName, visitTypeName,
                                              contacts)
    print(response_text)
