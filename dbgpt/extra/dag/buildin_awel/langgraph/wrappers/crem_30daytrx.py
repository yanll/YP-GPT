import requests

def get_customer_info(customer_id):
    url = 'https://cem.yeepay.com/cem-api/doggiex-daportal/wrap/apis/CEMCustomerPortraitCustomerInfo_30DaysTrxnew'
    headers = {
        'Yuiassotoken': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJsb2dpbl90eXBlIjoiQUNDT1VOVCIsIm1vYmlsZSI6IjE4NzU0MzE2MjQwIiwibWlncmF0ZV91c2VyX2lkIjoiZWM4Z2ExYWYiLCJ4LWlwIjoiMTcyLjI1LjI1LjEwIiwicHJpbmNpcGFsX2lkIjoiMTc3OTUiLCJ0b2tlbiI6ImViMDdmZmQyLTE4ZmYtNDU4Ny1hMTNjLWU2MmY2ZjY2NDdiNSIsImxvZ2luX25hbWUiOiJodWF4dWUuemhhbmciLCJ0d29fZmFjdG9yX3ZhbGlkIjp0cnVlLCJsb2dpbl90aW1lIjoiMjAyNC0wNC0yOSAxNDowMTo1MyIsInNjb3BlIjoiIiwiY2FsbGJhY2siOiJodHRwczovL25jY2VtcG9ydGFsLnllZXBheS5jb20vIy9jcm0vd29ya1JlcG9ydCIsInNzb3RpY2tldCI6IjU2M2U3NTUzLWY0NzktNDA5MC1iYzMwLTk0OTNjNTI2YzU2NiIsImV4cCI6MTcxNDQ1NjkxMywiaWF0IjoxNzE0MzY4NzEzLCJlbWFpbCI6Imh1YXh1ZS56aGFuZ0B5ZWVwYXkuY29tIiwidXNlcm5hbWUiOiLlvKDljY7pm6oifQ.RQj2jE214xsM6owBcK11npUmva18mOnzAYOqJ0RfoA_2N5Qxt7sA7I8pVR0cIFCah9mHXcX-3wJ-93tRFpENYg'  # 你的请求头信息
    }
    data = {
        "uid": "1191",
        "rid": "843",
        "querys": "{\"客户编号\":\"" + customer_id + "\",\"交易日期\":\"2024-03-30,2024-04-28\"}",
        "apiName": "CEMCustomerPortraitCustomerInfo_30DaysTrxnew",
        "limit": ""
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        json_data = response.json()
        if 'data' in json_data and 'data' in json_data['data'] and len(json_data['data']['data']) > 0:
            # 提取近30天毛利、近30天毛利排名、近30天交易金额和近30天支付成功率
            result = {
                "近30天毛利": json_data['data']['data'][0]['jin30tianmaoli'],
                "近30天毛利排名": json_data['data']['data'][0]['jin30tianmaolipaiming'],
                "近30天交易金额": json_data['data']['data'][0]['jin30tianjiaoyijine'],
                "近30天支付成功率": json_data['data']['data'][0]['jin30tianzhifuchenggonglv']
            }
            return result
        else:
            return {"error": "未找到相关数据"}
    else:
        return {"error": "请求失败，状态码：" + str(response.status_code)}

# 调用示例
customer_id = "KA2022-A09150004"  # 这里替换为你要查询的客户商编ID
result = get_customer_info(customer_id)
print(result)



customer_id = "KA2022-A09150004"