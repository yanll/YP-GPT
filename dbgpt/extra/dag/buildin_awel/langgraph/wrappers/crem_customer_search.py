import requests
import json
import requests
from dbgpt.util import envutils, consts
from dbgpt.util.lark import ssoutil


def customer_list_search(open_id: str, customer_name=None, customer_number=None):
    url = envutils.getenv("CREM_ENDPOINT_PROD") + '/comprehensiveSearch/_search'
    headers = {
        'yuiassotoken': ssoutil.get_sso_credential(open_id=open_id),  # 确保这个 token 获取函数已经被正确定义
        'Content-Type': 'application/json',
    }

    # 检查输入参数，选择查询数据
    if customer_name:
        query_data = customer_name
    elif customer_number:
        query_data = customer_number
    else:
        return {"success": "false", "response_message": "Both customer_name and customer_number cannot be empty."}

    data = {
        "queryData": query_data,
        "pageSize": 5,
        "pageNum": 1
    }

    response = requests.post(url, headers=headers, data=json.dumps(data), timeout=consts.request_time_out)
    if response.status_code == 200:
        json_data = response.json()
        customers = json_data.get('data', {}).get('list', [])

        # 只提取需要的字段
        result = []
        for customer in customers:
            customer_info = {
                "customerName": customer.get("customerName"),
                "customerIntroduction": customer.get("customerIntroduction", ""),
                "industryLine": customer.get("industryLine"),
                "saleName": customer.get("saleName"),
                "customerNo": customer.get("customerNo")
            }
            result.append(customer_info)
        return result  # 返回提取后的数据
    else:
        return response.text  # 返回非成功状态码的响应正文

# # 示例调用
# # 你需要至少提供一个参数: customer_name 或 customer_number
# result = customer_list_search(customer_name="上海")
# for item in result:
#     print(item)
