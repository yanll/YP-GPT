import requests
from dbgpt.extra.dag.buildin_awel.langgraph.wrappers.crem_api_wrapper import getssotoken
from dbgpt.util import envutils
import datetime
def get_crem_30DaysTrxTre_card(customer_id):
    url = envutils.getenv("CREM_ENDPOINT") +'/doggiex-daportal/wrap/apis/CEMCustomerPortraitCustomerInfo_30DaysTrxTrenew'
    headers = {
        'yuiassotoken': getssotoken(),
        'Content-Type': 'application/json'
    }

    data = {

        "querys": "{\"客户编号\":\"" + customer_id + "\",\"商编交易日期\":\",\"}",
        "apiName": "CEMCustomerPortraitCustomerInfo_30DaysTrxTrenew",
        "limit": ""
    }

    # 发出 POST 请求
    response = requests.post(url, headers=headers, json=data)

    # 返回结果
    if response.status_code == 200:
        json_data = response.json()
    else:
        json_data = {"error": f"请求失败，状态码：{response.status_code}"}

    # 提取所需字段并转换为生成图表所需的格式
    if 'data' in json_data and 'data' in json_data['data']:
        formatted_data = []
        formatted_data_jiaoyijine = []
        for item in json_data['data']['data']:
            formatted_item_maoli = {
                "time": item["jiaoyiriqi"],  # 将交易日期作为 time
                "value": item["maoli"]  # 将毛利作为 value
            }
            formatted_item_jiaoyijine = {
                "time": item["jiaoyiriqi"],  # 将交易日期作为 time
                "value": item["jiaoyijine"]  # 将交易金额作为 value
            }
            formatted_data.append(formatted_item_maoli)
            formatted_data_jiaoyijine.append(formatted_item_jiaoyijine)
    else:
        formatted_data = []  # 如果没有数据或者请求失败，设置为空列表
        formatted_data_jiaoyijine = []  # 如果没有数据或者请求失败，设置为空列表

    # 图表配置1
    var = {
        "config": {},
        "i18n_elements": {
            "zh_cn": [
                {
                    "tag": "chart",
                    "chart_spec": {
                        "type": "area",
                        "title": {"text": "近30天毛利"},
                        "data": {"values": formatted_data},  # 更新数据部分
                        "xField": "time",
                        "yField": "value",
                    },
                }
            ]
        },
        "i18n_header": {}
    }

    # 图表配置2
    var2 = {
        "config": {},
        "i18n_elements": {
            "zh_cn": [
                {
                    "tag": "chart",
                    "chart_spec": {
                        "type": "area",
                        "title": {"text": "近30天交易金额"},
                        "data": {"values": formatted_data_jiaoyijine},  # 更新数据部分
                        "xField": "time",
                        "yField": "value",
                    },
                }
            ]
        },
        "i18n_header": {}
    }

    return json_data, formatted_data, formatted_data_jiaoyijine, var, var2


# # 示例调用
# customer_id = "KA2022-A09150004"
# customer_info, formatted_data, formatted_data_jiaoyijine, var, var2 = get_crem_30DaysTrxTre_card(customer_id)
# print("Customer Info:", customer_info)
# print("Formatted Data (Maoli):", formatted_data)
# print("Formatted Data (Jiaoyijine):", formatted_data_jiaoyijine)
# print("Var:", var)
# print("Var2:", var2)