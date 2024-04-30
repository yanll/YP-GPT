import requests
from dbgpt.extra.dag.buildin_awel.langgraph.wrappers.crem_api_wrapper import getssotoken
from dbgpt.util import envutils
def get_crem_30DaysTrxTre_card(customer_id):
    url = envutils.getenv("CREM_ENDPOINT") +'/doggiex-daportal/wrap/apis/CEMCustomerPortraitCustomerInfo_30DaysTrxTrenew'
    headers = {
        'yuiassotoken': getssotoken(),
        'Content-Type': 'application/json'
    }
    data = {
        "uid": "1191",
        "rid": "843",
        "querys": "{\"客户编号\":\"" + customer_id + "\",\"商编交易日期\":\"2024-03-30,2024-04-28\"}",
        "apiName": "CEMCustomerPortraitCustomerInfo_30DaysTrxTrenew",
        "limit": ""
    }

    response = requests.post(url, headers=headers, json=data)


    if response.status_code == 200:
        json_data = response.json()
        return json_data
    else:
        return {"error": "请求失败，状态码：" + str(response.status_code)}

