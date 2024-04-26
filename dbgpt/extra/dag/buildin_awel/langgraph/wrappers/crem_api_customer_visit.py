import requests
import json


#

def add_customer_visit_record(customer_name, followUpText, followUpTime, followUpTypeName, visitTypeName, contacts):
    url = 'https://nccemportal.yeepay.com/cem-api/busFollowUp/addCreateFollowUp'
    # url = "http://nck8s.iaas.yp:30762/cem-api/busFollowUp/addCreateFollowUp"

    headers = {
        'Yuiassotoken': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJsb2dpbl90eXBlIjoiQUNDT1VOVCIsIm1vYmlsZSI6IjE4NzU0MzE2MjQwIiwibWlncmF0ZV91c2VyX2lkIjoiZWM4Z2ExYWYiLCJ4LWlwIjoiMTcyLjI1LjI1LjEwIiwicHJpbmNpcGFsX2lkIjoiMTc3OTUiLCJ0b2tlbiI6IjljZDk1YTY4LTE5MzYtNDYxZS1hMjc2LWM1YjJkMzdjMzc0MSIsImxvZ2luX25hbWUiOiJodWF4dWUuemhhbmciLCJ0d29fZmFjdG9yX3ZhbGlkIjp0cnVlLCJsb2dpbl90aW1lIjoiMjAyNC0wNC0yNiAxNDowMjo0NyIsInNjb3BlIjoiIiwiY2FsbGJhY2siOiJodHRwczovL25jY2VtcG9ydGFsLnllZXBheS5jb20vIy9jcm0vY2x1ZXNDdXN0b21lciIsInNzb3RpY2tldCI6Ijk3NjI0NWY5LTU4MGMtNGUzNS1hNDdjLTljNDdiYWQ5YWVlMiIsImV4cCI6MTcxNDE5Nzc2NywiaWF0IjoxNzE0MTA5NTY3LCJlbWFpbCI6Imh1YXh1ZS56aGFuZ0B5ZWVwYXkuY29tIiwidXNlcm5hbWUiOiLlvKDljY7pm6oifQ.yG9Timl49q6SYZFisOEiNiNathUyN9UmSrPLDux3j33DFdMZyXZDjLjc_WBMwY3XbG9yiSZEyp23JYNfDtbRVw',
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
    customerName = "张华雪报单客户测试"
    followUpText = "测试24"
    followUpTime = "2024-04-26 14:36:57"
    followUpTypeName = "在外约谈"
    visitTypeName = "签约后日常拜访"
    contacts = "张先生"

    response_text = add_customer_visit_record(customerName, followUpText, followUpTime, followUpTypeName, visitTypeName,
                                              contacts)
    print(response_text)
