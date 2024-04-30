# 导入必要的模块
import requests
from dbgpt.extra.dag.buildin_awel.langgraph.wrappers.crem_30DaysTrxTre_card import get_crem_30DaysTrxTre_card  # 确保此模块路径正确

# 调用第一个代码文件中的函数来获取数据
customer_id = "KA2021-A11220743"
customer_info = get_crem_30DaysTrxTre_card(customer_id)

# 提取所需字段并转换为生成图表所需的格式
if 'data' in customer_info and 'data' in customer_info['data']:
    formatted_data = []
    for item in customer_info['data']['data']:
        formatted_item = {
            "time": item["jiaoyiriqi"],  # 将交易日期作为 time
            "value": item["maoli"]  # 将毛利作为 value
        }
        formatted_data.append(formatted_item)
else:
    formatted_data = []  # 如果没有数据或者请求失败，设置为空列表


# 提取所需字段并转换为生成图表所需的格式
if 'data' in customer_info and 'data' in customer_info['data']:
    formatted_data_jiaoyijine = []
    for item in customer_info['data']['data']:
        formatted_item = {
            "time": item["jiaoyiriqi"],  # 将交易日期作为 time
            "value": item["jiaoyijine"]  # 将交易金额作为 value
        }
        formatted_data_jiaoyijine.append(formatted_item)
else:
    formatted_data_jiaoyijine = []  # 如果没有数据或者请求失败，设置为空列表
# 图表配置
var = {
    "config": {},
    "i18n_elements": {
        "zh_cn": [
            {
                "tag": "chart",
                "chart_spec": {
                    "type": "area",
                    "title": {"text": "面积图"},
                    "data": {"values": formatted_data},  # 更新数据部分
                    "xField": "time",
                    "yField": "value",
                },
            }
        ]
    },
    "i18n_header": {}
}


var2 = {
    "config": {},
    "i18n_elements": {
        "zh_cn": [
            {
                "tag": "chart",
                "chart_spec": {
                    "type": "area",
                    "title": {"text": "面积图"},
                    "data": {"values": formatted_data_jiaoyijine},  # 更新数据部分
                    "xField": "time",
                    "yField": "value",
                },
            }
        ]
    },
    "i18n_header": {}
}

# 打印更新后的图表配置，可以根据实际需求使用这个配置生成图表
print(var)
