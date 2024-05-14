import requests
from dbgpt.util import envutils, consts
import datetime

from dbgpt.util.lark import ssoutil


def get_crem_30DaysTrxTre_card(open_id, customer_id, customerName):
    url = (envutils.getenv("CREM_ENDPOINT_PROD") +
           '/doggiex-daportal/wrap/apis/CEMCustomerPortraitCustomerInfo_30DaysTrxTrenew')
    headers = {
        'yuiassotoken': ssoutil.get_sso_credential(open_id),
        'Content-Type': 'application/json'
    }

    data = {

        "querys": "{\"客户编号\":\"" + customer_id + "\",\"商编交易日期\":\",\"}",
        "apiName": "CEMCustomerPortraitCustomerInfo_30DaysTrxTrenew",
        "limit": ""
    }

    # 发出 POST 请求
    response = requests.post(url, headers=headers, json=data, timeout=consts.request_time_out)

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
                        "title": {"text": customerName + " 近30天毛利"},
                        "data": {"values": formatted_data},  # 更新数据部分
                        "xField": "time",
                        "yField": "value",
                        "axes": [
                            {
                                "orient": 'left',
                                "title": {
                                    "visible": "true",
                                    "text": "单位（元）"
                                }
                            }
                        ],
                        # "tooltip": {
                        #     "visible": "true",
                        #     "dimension": {
                        #         "visible": "true",
                        #         "title": {
                        #             "visible": "true",
                        #             "value": "近30天毛利"
                        #         }
                        #     }
                        # },
                    },
                },
                {
                    "tag": "column_set",
                    "flex_mode": "none",
                    "background_style": "default",
                    "horizontal_spacing": "0px",
                    "horizontal_align": "left",
                    "columns": [
                        {
                            "tag": "column",
                            "width": "weighted",
                            "vertical_align": "top",
                            "vertical_spacing": "8px",
                            "background_style": "default",
                            "elements": [
                                {
                                    "tag": "button",
                                    "text": {
                                        "tag": "plain_text",
                                        "content": ""
                                    },
                                    "type": "primary_text",
                                    "complex_interaction": "true",
                                    "width": "default",
                                    "size": "medium",
                                    "icon": {
                                        "tag": "standard_icon",
                                        "token": "add-bold_outlined"
                                    },
                                    "hover_tips": {
                                        "tag": "plain_text",
                                        "content": "新会话"
                                    },
                                    "value": {
                                        "event_type": "new_chat"
                                    }
                                }
                            ],
                            "weight": 5
                        },
                        {
                            "tag": "column",
                            "width": "weighted",
                            "vertical_align": "top",
                            "vertical_spacing": "8px",
                            "background_style": "default",
                            "elements": [],
                            "weight": 1
                        },
                        {
                            "tag": "column",
                            "width": "weighted",
                            "vertical_align": "top",
                            "vertical_spacing": "8px",
                            "background_style": "default",
                            "elements": [],
                            "weight": 1
                        }
                    ],
                    "margin": "16px 0px 0px 0px"
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
                        "title": {"text": customerName + " 近30天交易金额"},
                        "data": {"values": formatted_data_jiaoyijine},  # 更新数据部分
                        "xField": "time",
                        "yField": "value",
                        "axes": [
                            {
                                "orient": 'left',
                                "title": {
                                    "visible": "true",
                                    "text": "单位（元）"
                                }
                            }
                        ],

                    },
                },
                {
                    "tag": "column_set",
                    "flex_mode": "none",
                    "background_style": "default",
                    "horizontal_spacing": "0px",
                    "horizontal_align": "left",
                    "columns": [
                        {
                            "tag": "column",
                            "width": "weighted",
                            "vertical_align": "top",
                            "vertical_spacing": "8px",
                            "background_style": "default",
                            "elements": [
                                {
                                    "tag": "button",
                                    "text": {
                                        "tag": "plain_text",
                                        "content": ""
                                    },
                                    "type": "primary_text",
                                    "complex_interaction": "true",
                                    "width": "default",
                                    "size": "medium",
                                    "icon": {
                                        "tag": "standard_icon",
                                        "token": "add-bold_outlined"
                                    },
                                    "hover_tips": {
                                        "tag": "plain_text",
                                        "content": "新会话"
                                    },
                                    "value": {
                                        "event_type": "new_chat"
                                    }
                                }
                            ],
                            "weight": 5
                        },
                        {
                            "tag": "column",
                            "width": "weighted",
                            "vertical_align": "top",
                            "vertical_spacing": "8px",
                            "background_style": "default",
                            "elements": [],
                            "weight": 1
                        },
                        {
                            "tag": "column",
                            "width": "weighted",
                            "vertical_align": "top",
                            "vertical_spacing": "8px",
                            "background_style": "default",
                            "elements": [],
                            "weight": 1
                        }
                    ],
                    "margin": "16px 0px 0px 0px"
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
