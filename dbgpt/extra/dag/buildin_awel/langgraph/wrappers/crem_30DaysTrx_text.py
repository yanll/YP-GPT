import requests
from dbgpt.extra.dag.buildin_awel.langgraph.wrappers.crem_api_wrapper import getssotoken
from dbgpt.util import envutils
def get_crem_30DaysTrx_text(customer_id):
    url = envutils.getenv("CREM_ENDPOINT") +'/doggiex-daportal/wrap/apis/CEMCustomerPortraitCustomerInfo_30DaysTrxnew'
    headers = {
        'yuiassotoken': getssotoken(),
        'Content-Type': 'application/json'
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
result = get_crem_30DaysTrx_text(customer_id)
print(result)



