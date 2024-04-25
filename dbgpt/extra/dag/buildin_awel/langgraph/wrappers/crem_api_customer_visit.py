import requests
import json


def add_customer_visit_record(customerName, followUpText, followUpTime, followUpTypeName, visitTypeName):
    # url = "https://nccemportal.yeepay.com/cem-api/busFollowUp/addCreateFollowUp"
    url = "http://nck8s.iaas.yp:30762/cem-api/busFollowUp/addCreateFollowUp"
    headers = {
        "Content-Type": "application/json",

        "Cookie": "JSESSIONID=1FDA3D0966837001D034C6038280C676",
        "Yuiassotoken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJsb2dpbl90eXBlIjoiQUNDT1VOVCIsIm1vYmlsZSI6IjE4NzU0MzE2MjQwIiwibWlncmF0ZV91c2VyX2lkIjoiZWM4Z2ExYWYiLCJ4LWlwIjoiMTcyLjI1LjI1LjEwIiwicHJpbmNpcGFsX2lkIjoiMTc3OTUiLCJ0b2tlbiI6ImM3MmZiZWMwLTk5YTMtNDBkOC1hYTM5LTRlZWVlZjE0ZGU0NCIsImxvZ2luX25hbWUiOiJodWF4dWUuemhhbmciLCJ0d29fZmFjdG9yX3ZhbGlkIjp0cnVlLCJsb2dpbl90aW1lIjoiMjAyNC0wNC0yNSAxNDowNTo1NiIsInNjb3BlIjoiIiwiY2FsbGJhY2siOiJodHRwczovL25jY2VtcG9ydGFsLnllZXBheS5jb20vIy9jcm0vZm9sbG93VmlzaXQiLCJzc290aWNrZXQiOiI3YzFhNWZmNi1iMzVjLTQxMTgtYWRhMi02YWI4M2UxZTY3ZTIiLCJleHAiOjE3MTQxMTE1NTYsImlhdCI6MTcxNDAyMzM1NiwiZW1haWwiOiJodWF4dWUuemhhbmdAeWVlcGF5LmNvbSIsInVzZXJuYW1lIjoi5byg5Y2O6ZuqIn0.AnkI7Mp6sC8i3i - GlEPU1_VGa95amO_pJjje4ExBrgX3Vx6C4ezNRdZRyzSFWCyID1c73PnDqsT_P5puGjrsnA",
          }



    data = {

    "customerName": "测试张华雪222",
    "customerNo": "KA2024-A04250001",
    "followUpText": "测试20",
    "followUpTime": "2024-04-25 18:07:19",
    "followUpTypeName": "客户公司拜访",
    "visitTypeName": "签约后日常拜访",
    "type": 1,
    "headEntityKey": "followUpInfo"
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()


