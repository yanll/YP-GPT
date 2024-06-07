import json

import requests
from dbgpt.util import envutils, consts
from datetime import datetime, timedelta

from dbgpt.util.lark import ssoutil, lark_message_util

def get_previous_dates():
    today = datetime.now()  #今天
    yesterday_all = today - timedelta(days=1) #昨天
    yesterday = yesterday_all.strftime('%Y-%m-%d')
    print("昨天", yesterday)
    day8_before_yesterday_all = today - timedelta(days=8)#8天前
    day8_before_yesterday = day8_before_yesterday_all.strftime('%Y-%m-%d')
    print("昨天的8天前",day8_before_yesterday)
    num_day8_before_yesterday = f"{day8_before_yesterday},{yesterday}"
    print("近8天", num_day8_before_yesterday)
    ''''''

    day31_before_yesterday_all = today - timedelta(days=31)  # 8天前
    day31_before_yesterday = day31_before_yesterday_all.strftime('%Y-%m-%d')
    print("昨天的31天前", day31_before_yesterday)
    num_day31_before_yesterday = f"{day31_before_yesterday},{yesterday}"
    print("近31天", num_day31_before_yesterday)
    return num_day8_before_yesterday ,num_day31_before_yesterday





def get_crem_hanglv_merchant_8days_transaction_search_card(open_id,nickname,customer_no):
    num_day8_before_yesterday,num_day31_before_yesterday = get_previous_dates()
    url = (envutils.getenv("CREM_ENDPOINT_PROD") +
           '/aggScript/wrap/apis/receive/handleApplicationMarketplace/dealSizeLook')
    headers = {
        'yuiassotoken': ssoutil.get_sso_credential(open_id),
        'Content-Type': 'application/json',
        'pageType': 'cemPortal'

    }
    data = {
    "parameters": {
        "STAT_SALES_NAME": nickname,
        "TYPE": "航司,渠道,酒旅出行",
        "TRX_DATE": num_day8_before_yesterday,
        "SCALE_TYPE": "DAY",
        "STAT_DISPAYSIGNEDNAME": customer_no
    },
    "strategyKey": "saleOrdinaryApplicationMarketExecutor"
}
    # 发出 POST 请求
    response = requests.post(url, headers=headers, json=data)

    # 处理 API 响应数据
    api_data = json.loads(response.text)
    print("原始数据",api_data)



    # 转换并格式化数据
    formatted_data = []
    for entry in api_data["data"]["data"]:

        amount_entry = {
            "TRX_DATE": entry["trxDate"],
            "type": "交易净额",
            "TRX_TRUE_AMOUNT": round(float(entry["trueAmount"]) / 10000, 2)
        }
        profit_entry = {
            "TRX_DATE": entry["trxDate"],
            "type": "毛利",
            "TRX_PROFIT": round(float(entry["profit"]) / 10000, 2)
        }
        formatted_data.extend([profit_entry, amount_entry])

    print(formatted_data)


    # 生成完整的数据
    complete_data_8days_TRX_TRUE_AMOUNT = [
                        # 交易净额
                        {"TRX_DATE": entry["TRX_DATE"], "type": "交易净额", "TRX_TRUE_AMOUNT": entry["TRX_TRUE_AMOUNT"]}
                        for entry in formatted_data if entry["type"] == "交易净额"
                    ]
    print("8天毛利数据",complete_data_8days_TRX_TRUE_AMOUNT)

    complete_data_8days_TRX_PROFIT = [
                        # 毛利
                        {"TRX_DATE": entry["TRX_DATE"], "type": "毛利", "TRX_PROFIT": entry["TRX_PROFIT"]}
                        for entry in formatted_data if entry["type"] == "毛利"
                    ]

    print("8天毛利数据",complete_data_8days_TRX_PROFIT)


    var_8_TRX_TRUE_AMOUNT = {
        "config": {},
        "i18n_elements": {
            "zh_cn": [
                {
                    "tag": "chart",
                    "chart_spec": {
                        "type": "area",
                        "title": {
                            "text": "近8天交易表现" + "——交易净额——" +customer_no
                        },
                        "data": {
                            "values":
                                complete_data_8days_TRX_TRUE_AMOUNT},  # 更新数据部分

                        "xField": "TRX_DATE",
                        "yField": "TRX_TRUE_AMOUNT",
                        "seriesField": "type",
                        "axes": [
                            {
                                "orient": "left",
                                "title": {
                                    "visible": "true",
                                    "text": "单位（万）"
                                }
                            }
                        ],
                        "legends": [
                            {
                                "visible": "true",
                                "position": "middle",
                                "orient": "bottom"
                            }
                        ],
                        "stack": "false",
                        "areaStyle": {
                            "fillOpacity": 0.5
                        },
                        "lineStyle": {
                            "strokeWidth": 2
                        }
                    }
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

    var_8_TRX_PROFIT = {
        "config": {},
        "i18n_elements": {
            "zh_cn": [
                {
                    "tag": "chart",
                    "chart_spec": {
                        "type": "area",
                        "title": {
                            "text": "近8天交易表现" + "——毛利——" +customer_no
                        },
                        "data": {
                            "values":
                                complete_data_8days_TRX_PROFIT},  # 更新数据部分

                        "xField": "TRX_DATE",
                        "yField": "TRX_PROFIT",
                        "seriesField": "type",
                        "axes": [
                            {
                                "orient": "left",
                                "title": {
                                    "visible": "true",
                                    "text": "单位（万）"
                                }
                            }
                        ],
                        "legends": [
                            {
                                "visible": "true",
                                "position": "middle",
                                "orient": "bottom"
                            }
                        ],
                        "stack": "false",
                        "areaStyle": {
                            "fillOpacity": 0.5
                        },
                        "lineStyle": {
                            "strokeWidth": 2
                        }
                    }
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

    lark_message_util.send_card_message(
        receive_id=open_id,
        content=var_8_TRX_TRUE_AMOUNT
    )
    lark_message_util.send_card_message(
        receive_id=open_id,
        content=var_8_TRX_PROFIT
    )

# get_crem_hanglv_merchant_8days_transaction_search_card("ou_9d42bb88ec8940baf3ad183755131881","段超","CA")


def get_crem_hanglv_merchant_31days_transaction_search_card(open_id,nickname,customer_no):
    num_day8_before_yesterday, num_day31_before_yesterday = get_previous_dates()
    url = (envutils.getenv("CREM_ENDPOINT_PROD") +
           '/aggScript/wrap/apis/receive/handleApplicationMarketplace/dealSizeLook')
    headers = {
        'yuiassotoken': ssoutil.get_sso_credential(open_id),
        'Content-Type': 'application/json',
        'pageType': 'cemPortal'

    }
    data = {
        "parameters": {
            "STAT_SALES_NAME": nickname,
            "TYPE": "航司,渠道,酒旅出行",
            "TRX_DATE": num_day31_before_yesterday,
            "SCALE_TYPE": "DAY",
            "STAT_DISPAYSIGNEDNAME": customer_no
        },
        "strategyKey": "saleOrdinaryApplicationMarketExecutor"
    }
    # 发出 POST 请求
    response = requests.post(url, headers=headers, json=data)

    # 处理 API 响应数据
    api_data = json.loads(response.text)
    print("原始数据", api_data)

    # 转换并格式化数据
    formatted_data = []
    for entry in api_data["data"]["data"]:
        amount_entry = {
            "TRX_DATE": entry["trxDate"],
            "type": "交易净额",
            "TRX_TRUE_AMOUNT": round(float(entry["trueAmount"]) / 10000, 2)
        }
        profit_entry = {
            "TRX_DATE": entry["trxDate"],
            "type": "毛利",
            "TRX_PROFIT": round(float(entry["profit"]) / 10000, 2)
        }
        formatted_data.extend([profit_entry, amount_entry])

    print(formatted_data)


    # 生成完整的数据
    complete_data_8days_TRX_TRUE_AMOUNT = [
                        # 交易净额
                        {"TRX_DATE": entry["TRX_DATE"], "type": "交易净额", "TRX_TRUE_AMOUNT": entry["TRX_TRUE_AMOUNT"]}
                        for entry in formatted_data if entry["type"] == "交易净额"
                    ]
    print("8天毛利数据",complete_data_8days_TRX_TRUE_AMOUNT)

    complete_data_8days_TRX_PROFIT = [
                        # 毛利
                        {"TRX_DATE": entry["TRX_DATE"], "type": "毛利", "TRX_PROFIT": entry["TRX_PROFIT"]}
                        for entry in formatted_data if entry["type"] == "毛利"
                    ]

    print("8天毛利数据",complete_data_8days_TRX_PROFIT)


    var_8_TRX_TRUE_AMOUNT = {
        "config": {},
        "i18n_elements": {
            "zh_cn": [
                {
                    "tag": "chart",
                    "chart_spec": {
                        "type": "area",
                        "title": {
                            "text": "近31天交易表现" + "——交易净额——" +customer_no
                        },
                        "data": {
                            "values":
                                complete_data_8days_TRX_TRUE_AMOUNT},  # 更新数据部分

                        "xField": "TRX_DATE",
                        "yField": "TRX_TRUE_AMOUNT",
                        "seriesField": "type",
                        "axes": [
                            {
                                "orient": "left",
                                "title": {
                                    "visible": "true",
                                    "text": "单位（万）"
                                }
                            }
                        ],
                        "legends": [
                            {
                                "visible": "true",
                                "position": "middle",
                                "orient": "bottom"
                            }
                        ],
                        "stack": "false",
                        "areaStyle": {
                            "fillOpacity": 0.5
                        },
                        "lineStyle": {
                            "strokeWidth": 2
                        }
                    }
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

    var_8_TRX_PROFIT = {
        "config": {},
        "i18n_elements": {
            "zh_cn": [
                {
                    "tag": "chart",
                    "chart_spec": {
                        "type": "area",
                        "title": {
                            "text": "近31天交易表现" + "——毛利——" +customer_no
                        },
                        "data": {
                            "values":
                                complete_data_8days_TRX_PROFIT},  # 更新数据部分

                        "xField": "TRX_DATE",
                        "yField": "TRX_PROFIT",
                        "seriesField": "type",
                        "axes": [
                            {
                                "orient": "left",
                                "title": {
                                    "visible": "true",
                                    "text": "单位（万）"
                                }
                            }
                        ],
                        "legends": [
                            {
                                "visible": "true",
                                "position": "middle",
                                "orient": "bottom"
                            }
                        ],
                        "stack": "false",
                        "areaStyle": {
                            "fillOpacity": 0.5
                        },
                        "lineStyle": {
                            "strokeWidth": 2
                        }
                    }
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

    lark_message_util.send_card_message(
        receive_id=open_id,
        content=var_8_TRX_TRUE_AMOUNT
    )
    lark_message_util.send_card_message(
        receive_id=open_id,
        content=var_8_TRX_PROFIT
    )

# get_crem_hanglv_merchant_31days_transaction_search_card("ou_9d42bb88ec8940baf3ad183755131881", "段超","CA")






def get_crem_hanglv_merchant_8days_product_search_card(open_id,nickname,customer_no):
    num_day8_before_yesterday,num_day31_before_yesterday = get_previous_dates()
    url = (envutils.getenv("CREM_ENDPOINT_PROD") +
           '/threeParty/wrap/apis/agg/productline_pcd_sh8daystrx')
    headers = {
        'yuiassotoken': ssoutil.get_sso_credential(open_id),
        'Content-Type': 'application/json',
        'pageType': 'cemPortal'

    }

    data = {
                "tenant": "default",
                "procDefKey": "15a8350f65a303736ebe606e3d30e5beM5",
                "data": {
                    "dmallReq": {
                        "parameters": {
                            "TRX_DATE": num_day8_before_yesterday,
                            "TYPE": "全部",
                            "PRODUCTTYPE": "会员,旗舰店,收单,航旅快捷",
                            "SUPERIOR_NAME": nickname,
                            "STAT_SALES_NAME": nickname,
                            "STAT_DISPAYSIGNEDNAME": customer_no
                        },
                        "url": "productline_pcd_hl_zt_sh8daystrx",
                        "version": "V1.0"
                    }
                }
            }





    # 发出 POST 请求
    response = requests.post(url, headers=headers, json=data, timeout=consts.request_time_out)

    # 处理 API 响应数据
    api_data = json.loads(response.text)
    print("原始数据",api_data)

    # 将利润转换为万元并格式化数据
    formatted_data = [
        {
            "type": entry["PRODUCTTYPE"],
            "trxDate": entry["TRX_DATE"],
            "profit": round(float(entry["TRX_PROFIT"]) / 10000, 2)  # 将利润转换为万元并保留两位小数
        }
        for entry in api_data["data"]["data"]
    ]

    # 生成完整的数据
    complete_data = [
                        # 会员
                        {"trxDate": entry["trxDate"], "type": "会员", "profit": entry["profit"]}
                        for entry in formatted_data if entry["type"] == "会员"
                    ] + [
                        # 旗舰店
                        {"trxDate": entry["trxDate"], "type": "旗舰店", "profit": entry["profit"]}
                        for entry in formatted_data if entry["type"] == "旗舰店"
                    ] + [
                        # 航旅快捷
                        {"trxDate": entry["trxDate"], "type": "航旅快捷", "profit": entry["profit"]}
                        for entry in formatted_data if entry["type"] == "航旅快捷"
                    ]

    print("完整的数据格式是",complete_data)

    var = {
        "config": {},
        "i18n_elements": {
            "zh_cn": [
                {
                    "tag": "chart",
                    "chart_spec": {
                        "type": "area",
                        "title": {
                            "text": "近8天产品表现"+"——毛利——"+customer_no
                        },
                        "data": {
                            "values":
                                complete_data},  # 更新数据部分

                        "xField": "trxDate",
                        "yField": "profit",
                        "seriesField": "type",
                        "axes": [
                            {
                                "orient": "left",
                                "title": {
                                    "visible": "true",
                                    "text": "单位（万）"
                                }
                            }
                        ],
                        "legends": [
                            {
                                "visible": "true",
                                "position": "middle",
                                "orient": "bottom"
                            }
                        ],
                        "stack": "false",
                        "areaStyle": {
                            "fillOpacity": 0.5
                        },
                        "lineStyle": {
                            "strokeWidth": 2
                        }
                    }
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

    lark_message_util.send_card_message(
        receive_id=open_id,
        content=var
    )


# get_crem_hanglv_merchant_8days_product_search_card("ou_9d42bb88ec8940baf3ad183755131881","段超","CA")

def get_crem_hanglv_merchant_31days_product_search_card(open_id,nickname,customer_no):
    num_day8_before_yesterday,num_day31_before_yesterday = get_previous_dates()
    url = (envutils.getenv("CREM_ENDPOINT_PROD") +
           '/threeParty/wrap/apis/agg/productline_pcd_sh8daystrx')
    headers = {
        'yuiassotoken': ssoutil.get_sso_credential(open_id),
        'Content-Type': 'application/json',
        'pageType': 'cemPortal'

    }

    data = {
                "tenant": "default",
                "procDefKey": "15a8350f65a303736ebe606e3d30e5beM5",
                "data": {
                    "dmallReq": {
                        "parameters": {
                            "TRX_DATE": num_day31_before_yesterday,
                            "TYPE": "全部",
                            "PRODUCTTYPE": "会员,旗舰店,收单,航旅快捷",
                            "SUPERIOR_NAME": nickname,
                            "STAT_SALES_NAME": nickname,
                            "STAT_DISPAYSIGNEDNAME": customer_no
                        },
                        "url": "productline_pcd_hl_zt_sh8daystrx",
                        "version": "V1.0"
                    }
                }
            }





    # 发出 POST 请求
    response = requests.post(url, headers=headers, json=data, timeout=consts.request_time_out)

    # 处理 API 响应数据
    api_data = json.loads(response.text)
    print("原始数据",api_data)

    # 将利润转换为万元并格式化数据
    formatted_data = [
        {
            "type": entry["PRODUCTTYPE"],
            "trxDate": entry["TRX_DATE"],
            "profit": round(float(entry["TRX_PROFIT"]) / 10000, 2)  # 将利润转换为万元并保留两位小数
        }
        for entry in api_data["data"]["data"]
    ]

    # 生成完整的数据
    complete_data = [
                        # 会员
                        {"trxDate": entry["trxDate"], "type": "会员", "profit": entry["profit"]}
                        for entry in formatted_data if entry["type"] == "会员"
                    ] + [
                        # 旗舰店
                        {"trxDate": entry["trxDate"], "type": "旗舰店", "profit": entry["profit"]}
                        for entry in formatted_data if entry["type"] == "旗舰店"
                    ] + [
                        # 航旅快捷
                        {"trxDate": entry["trxDate"], "type": "航旅快捷", "profit": entry["profit"]}
                        for entry in formatted_data if entry["type"] == "航旅快捷"
                    ]

    print("完整的数据格式是",complete_data)

    var = {
        "config": {},
        "i18n_elements": {
            "zh_cn": [
                {
                    "tag": "chart",
                    "chart_spec": {
                        "type": "area",
                        "title": {
                            "text": "近31天产品表现"+"——毛利——"+customer_no
                        },
                        "data": {
                            "values":
                                complete_data},  # 更新数据部分

                        "xField": "trxDate",
                        "yField": "profit",
                        "seriesField": "type",
                        "axes": [
                            {
                                "orient": "left",
                                "title": {
                                    "visible": "true",
                                    "text": "单位（万）"
                                }
                            }
                        ],
                        "legends": [
                            {
                                "visible": "true",
                                "position": "middle",
                                "orient": "bottom"
                            }
                        ],
                        "stack": "false",
                        "areaStyle": {
                            "fillOpacity": 0.5
                        },
                        "lineStyle": {
                            "strokeWidth": 2
                        }
                    }
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

    lark_message_util.send_card_message(
        receive_id=open_id,
        content=var
    )


#get_crem_hanglv_merchant_31days_product_search_card("ou_9d42bb88ec8940baf3ad183755131881","段超")





















# def get_crem_hanglv_merchant_8days_transaction_search_card(open_id,nickname,customer_no):
#     num_day8_before_yesterday,num_day31_before_yesterday = get_previous_dates()
#     url = (envutils.getenv("CREM_ENDPOINT_PROD") +
#            '/threeParty/wrap/apis/agg/productline_pcd_sh8daystrx')
#     headers = {
#         'yuiassotoken': ssoutil.get_sso_credential(open_id),
#         'Content-Type': 'application/json',
#         'pageType': 'cemPortal'
#
#     }
#     data = {
#     "tenant": "default",
#     "procDefKey": "15a8350f65a303736ebe606e3d30e5beM5",
#     "data": {
#         "dmallReq": {
#             "parameters": {
#                 "TRX_DATE": num_day8_before_yesterday,
#                 "TYPE": "全部",
#                 "SUPERIOR_NAME": nickname,
#                 "STAT_SALES_NAME": nickname,
#                 "STAT_DISPAYSIGNEDNAME": customer_no
#             },
#             "url": "productline_pcd_hl_zt_sh8daystrx",
#             "version": "V1.0"
#         }
#     }
# }
#     # 发出 POST 请求
#     response = requests.post(url, headers=headers, json=data, timeout=consts.request_time_out)
#
#     # 处理 API 响应数据
#     api_data = json.loads(response.text)
#     print("原始数据",api_data)
#
#
#
#     # 转换并格式化数据
#     formatted_data = []
#     for entry in api_data["data"]["data"]:
#
#         amount_entry = {
#             "TRX_DATE": entry["TRX_DATE"],
#             "type": "交易净额",
#             "TRX_TRUE_AMOUNT": round(float(entry["TRX_TRUE_AMOUNT"]) / 10000, 2)
#         }
#         profit_entry = {
#             "TRX_DATE": entry["TRX_DATE"],
#             "type": "毛利",
#             "TRX_PROFIT": round(float(entry["TRX_PROFIT"]) / 10000, 2)
#         }
#         formatted_data.extend([profit_entry, amount_entry])
#
#     print(formatted_data)
#
#
#     # 生成完整的数据
#     complete_data_8days_TRX_TRUE_AMOUNT = [
#                         # 交易净额
#                         {"TRX_DATE": entry["TRX_DATE"], "type": "交易净额", "TRX_TRUE_AMOUNT": entry["TRX_TRUE_AMOUNT"]}
#                         for entry in formatted_data if entry["type"] == "交易净额"
#                     ]
#     print("8天毛利数据",complete_data_8days_TRX_TRUE_AMOUNT)
#
#     complete_data_8days_TRX_PROFIT = [
#                         # 毛利
#                         {"TRX_DATE": entry["TRX_DATE"], "type": "毛利", "TRX_PROFIT": entry["TRX_PROFIT"]}
#                         for entry in formatted_data if entry["type"] == "毛利"
#                     ]
#
#     print("8天毛利数据",complete_data_8days_TRX_PROFIT)
#
#
#     var_8_TRX_TRUE_AMOUNT = {
#         "config": {},
#         "i18n_elements": {
#             "zh_cn": [
#                 {
#                     "tag": "chart",
#                     "chart_spec": {
#                         "type": "area",
#                         "title": {
#                             "text": "近8天交易表现" + "——交易净额——" +customer_no
#                         },
#                         "data": {
#                             "values":
#                                 complete_data_8days_TRX_TRUE_AMOUNT},  # 更新数据部分
#
#                         "xField": "TRX_DATE",
#                         "yField": "TRX_TRUE_AMOUNT",
#                         "seriesField": "type",
#                         "axes": [
#                             {
#                                 "orient": "left",
#                                 "title": {
#                                     "visible": "true",
#                                     "text": "单位（万）"
#                                 }
#                             }
#                         ],
#                         "legends": [
#                             {
#                                 "visible": "true",
#                                 "position": "middle",
#                                 "orient": "bottom"
#                             }
#                         ],
#                         "stack": "false",
#                         "areaStyle": {
#                             "fillOpacity": 0.5
#                         },
#                         "lineStyle": {
#                             "strokeWidth": 2
#                         }
#                     }
#                 },
#                 {
#                     "tag": "column_set",
#                     "flex_mode": "none",
#                     "background_style": "default",
#                     "horizontal_spacing": "0px",
#                     "horizontal_align": "left",
#                     "columns": [
#                         {
#                             "tag": "column",
#                             "width": "weighted",
#                             "vertical_align": "top",
#                             "vertical_spacing": "8px",
#                             "background_style": "default",
#                             "elements": [
#                                 {
#                                     "tag": "button",
#                                     "text": {
#                                         "tag": "plain_text",
#                                         "content": ""
#                                     },
#                                     "type": "primary_text",
#                                     "complex_interaction": "true",
#                                     "width": "default",
#                                     "size": "medium",
#                                     "icon": {
#                                         "tag": "standard_icon",
#                                         "token": "add-bold_outlined"
#                                     },
#                                     "hover_tips": {
#                                         "tag": "plain_text",
#                                         "content": "新会话"
#                                     },
#                                     "value": {
#                                         "event_type": "new_chat"
#                                     }
#                                 }
#                             ],
#                             "weight": 5
#                         },
#                         {
#                             "tag": "column",
#                             "width": "weighted",
#                             "vertical_align": "top",
#                             "vertical_spacing": "8px",
#                             "background_style": "default",
#                             "elements": [],
#                             "weight": 1
#                         },
#                         {
#                             "tag": "column",
#                             "width": "weighted",
#                             "vertical_align": "top",
#                             "vertical_spacing": "8px",
#                             "background_style": "default",
#                             "elements": [],
#                             "weight": 1
#                         }
#                     ],
#                     "margin": "16px 0px 0px 0px"
#                 }
#             ]
#         },
#         "i18n_header": {}
#     }
#
#     var_8_TRX_PROFIT = {
#         "config": {},
#         "i18n_elements": {
#             "zh_cn": [
#                 {
#                     "tag": "chart",
#                     "chart_spec": {
#                         "type": "area",
#                         "title": {
#                             "text": "近8天交易表现" + "——毛利——" +customer_no
#                         },
#                         "data": {
#                             "values":
#                                 complete_data_8days_TRX_PROFIT},  # 更新数据部分
#
#                         "xField": "TRX_DATE",
#                         "yField": "TRX_PROFIT",
#                         "seriesField": "type",
#                         "axes": [
#                             {
#                                 "orient": "left",
#                                 "title": {
#                                     "visible": "true",
#                                     "text": "单位（万）"
#                                 }
#                             }
#                         ],
#                         "legends": [
#                             {
#                                 "visible": "true",
#                                 "position": "middle",
#                                 "orient": "bottom"
#                             }
#                         ],
#                         "stack": "false",
#                         "areaStyle": {
#                             "fillOpacity": 0.5
#                         },
#                         "lineStyle": {
#                             "strokeWidth": 2
#                         }
#                     }
#                 },
#                 {
#                     "tag": "column_set",
#                     "flex_mode": "none",
#                     "background_style": "default",
#                     "horizontal_spacing": "0px",
#                     "horizontal_align": "left",
#                     "columns": [
#                         {
#                             "tag": "column",
#                             "width": "weighted",
#                             "vertical_align": "top",
#                             "vertical_spacing": "8px",
#                             "background_style": "default",
#                             "elements": [
#                                 {
#                                     "tag": "button",
#                                     "text": {
#                                         "tag": "plain_text",
#                                         "content": ""
#                                     },
#                                     "type": "primary_text",
#                                     "complex_interaction": "true",
#                                     "width": "default",
#                                     "size": "medium",
#                                     "icon": {
#                                         "tag": "standard_icon",
#                                         "token": "add-bold_outlined"
#                                     },
#                                     "hover_tips": {
#                                         "tag": "plain_text",
#                                         "content": "新会话"
#                                     },
#                                     "value": {
#                                         "event_type": "new_chat"
#                                     }
#                                 }
#                             ],
#                             "weight": 5
#                         },
#                         {
#                             "tag": "column",
#                             "width": "weighted",
#                             "vertical_align": "top",
#                             "vertical_spacing": "8px",
#                             "background_style": "default",
#                             "elements": [],
#                             "weight": 1
#                         },
#                         {
#                             "tag": "column",
#                             "width": "weighted",
#                             "vertical_align": "top",
#                             "vertical_spacing": "8px",
#                             "background_style": "default",
#                             "elements": [],
#                             "weight": 1
#                         }
#                     ],
#                     "margin": "16px 0px 0px 0px"
#                 }
#             ]
#         },
#         "i18n_header": {}
#     }
#
#     lark_message_util.send_card_message(
#         receive_id=open_id,
#         content=var_8_TRX_TRUE_AMOUNT
#     )
#     lark_message_util.send_card_message(
#         receive_id=open_id,
#         content=var_8_TRX_PROFIT
#     )
#
# #get_crem_hanglv_merchant_8days_search_card("ou_079964d3b15f58fc330058a629b8ed41","段超")
#
#
# def get_crem_hanglv_merchant_31days_transaction_search_card(open_id,nickname,customer_no):
#     num_day8_before_yesterday,num_day31_before_yesterday = get_previous_dates()
#
#     url = (envutils.getenv("CREM_ENDPOINT_PROD") +
#            '/threeParty/wrap/apis/agg/productline_pcd_sh8daystrx')
#     headers = {
#         'yuiassotoken': ssoutil.get_sso_credential(open_id),
#         'Content-Type': 'application/json',
#         'pageType': 'cemPortal'
#
#     }
#     data = {
#     "tenant": "default",
#     "procDefKey": "15a8350f65a303736ebe606e3d30e5beM5",
#     "data": {
#         "dmallReq": {
#             "parameters": {
#                 "TRX_DATE": num_day31_before_yesterday,
#                 "TYPE": "全部",
#                 "SUPERIOR_NAME": nickname,
#                 "STAT_SALES_NAME": nickname,
#                 "STAT_DISPAYSIGNEDNAME": customer_no
#             },
#             "url": "productline_pcd_hl_zt_sh8daystrx",
#             "version": "V1.0"
#         }
#     }
# }
#     # 发出 POST 请求
#     response = requests.post(url, headers=headers, json=data, timeout=consts.request_time_out)
#
#     # 处理 API 响应数据
#     api_data = json.loads(response.text)
#     print("原始数据",api_data)
#
#
#
#     # 转换并格式化数据
#     formatted_data = []
#     for entry in api_data["data"]["data"]:
#
#         amount_entry = {
#             "TRX_DATE": entry["TRX_DATE"],
#             "type": "交易净额",
#             "TRX_TRUE_AMOUNT": round(float(entry["TRX_TRUE_AMOUNT"]) / 10000, 2)
#         }
#         profit_entry = {
#             "TRX_DATE": entry["TRX_DATE"],
#             "type": "毛利",
#             "TRX_PROFIT": round(float(entry["TRX_PROFIT"]) / 10000, 2)
#         }
#         formatted_data.extend([profit_entry, amount_entry])
#
#     print(formatted_data)
#
#
#     # 生成完整的数据
#     complete_data_8days_TRX_TRUE_AMOUNT = [
#                         # 交易净额
#                         {"TRX_DATE": entry["TRX_DATE"], "type": "交易净额", "TRX_TRUE_AMOUNT": entry["TRX_TRUE_AMOUNT"]}
#                         for entry in formatted_data if entry["type"] == "交易净额"
#                     ]
#     print("8天毛利数据",complete_data_8days_TRX_TRUE_AMOUNT)
#
#     complete_data_8days_TRX_PROFIT = [
#                         # 毛利
#                         {"TRX_DATE": entry["TRX_DATE"], "type": "毛利", "TRX_PROFIT": entry["TRX_PROFIT"]}
#                         for entry in formatted_data if entry["type"] == "毛利"
#                     ]
#
#     print("8天毛利数据",complete_data_8days_TRX_PROFIT)
#
#
#     var_8_TRX_TRUE_AMOUNT = {
#         "config": {},
#         "i18n_elements": {
#             "zh_cn": [
#                 {
#                     "tag": "chart",
#                     "chart_spec": {
#                         "type": "area",
#                         "title": {
#                             "text": "近31天交易表现" + "——交易净额——" +customer_no
#                         },
#                         "data": {
#                             "values":
#                                 complete_data_8days_TRX_TRUE_AMOUNT},  # 更新数据部分
#
#                         "xField": "TRX_DATE",
#                         "yField": "TRX_TRUE_AMOUNT",
#                         "seriesField": "type",
#                         "axes": [
#                             {
#                                 "orient": "left",
#                                 "title": {
#                                     "visible": "true",
#                                     "text": "单位（万）"
#                                 }
#                             }
#                         ],
#                         "legends": [
#                             {
#                                 "visible": "true",
#                                 "position": "middle",
#                                 "orient": "bottom"
#                             }
#                         ],
#                         "stack": "false",
#                         "areaStyle": {
#                             "fillOpacity": 0.5
#                         },
#                         "lineStyle": {
#                             "strokeWidth": 2
#                         }
#                     }
#                 },
#                 {
#                     "tag": "column_set",
#                     "flex_mode": "none",
#                     "background_style": "default",
#                     "horizontal_spacing": "0px",
#                     "horizontal_align": "left",
#                     "columns": [
#                         {
#                             "tag": "column",
#                             "width": "weighted",
#                             "vertical_align": "top",
#                             "vertical_spacing": "8px",
#                             "background_style": "default",
#                             "elements": [
#                                 {
#                                     "tag": "button",
#                                     "text": {
#                                         "tag": "plain_text",
#                                         "content": ""
#                                     },
#                                     "type": "primary_text",
#                                     "complex_interaction": "true",
#                                     "width": "default",
#                                     "size": "medium",
#                                     "icon": {
#                                         "tag": "standard_icon",
#                                         "token": "add-bold_outlined"
#                                     },
#                                     "hover_tips": {
#                                         "tag": "plain_text",
#                                         "content": "新会话"
#                                     },
#                                     "value": {
#                                         "event_type": "new_chat"
#                                     }
#                                 }
#                             ],
#                             "weight": 5
#                         },
#                         {
#                             "tag": "column",
#                             "width": "weighted",
#                             "vertical_align": "top",
#                             "vertical_spacing": "8px",
#                             "background_style": "default",
#                             "elements": [],
#                             "weight": 1
#                         },
#                         {
#                             "tag": "column",
#                             "width": "weighted",
#                             "vertical_align": "top",
#                             "vertical_spacing": "8px",
#                             "background_style": "default",
#                             "elements": [],
#                             "weight": 1
#                         }
#                     ],
#                     "margin": "16px 0px 0px 0px"
#                 }
#             ]
#         },
#         "i18n_header": {}
#     }
#
#     var_8_TRX_PROFIT = {
#         "config": {},
#         "i18n_elements": {
#             "zh_cn": [
#                 {
#                     "tag": "chart",
#                     "chart_spec": {
#                         "type": "area",
#                         "title": {
#                             "text": "近31天交易表现" + "——毛利——" +customer_no
#                         },
#                         "data": {
#                             "values":
#                                 complete_data_8days_TRX_PROFIT},  # 更新数据部分
#
#                         "xField": "TRX_DATE",
#                         "yField": "TRX_PROFIT",
#                         "seriesField": "type",
#                         "axes": [
#                             {
#                                 "orient": "left",
#                                 "title": {
#                                     "visible": "true",
#                                     "text": "单位（万）"
#                                 }
#                             }
#                         ],
#                         "legends": [
#                             {
#                                 "visible": "true",
#                                 "position": "middle",
#                                 "orient": "bottom"
#                             }
#                         ],
#                         "stack": "false",
#                         "areaStyle": {
#                             "fillOpacity": 0.5
#                         },
#                         "lineStyle": {
#                             "strokeWidth": 2
#                         }
#                     }
#                 },
#                 {
#                     "tag": "column_set",
#                     "flex_mode": "none",
#                     "background_style": "default",
#                     "horizontal_spacing": "0px",
#                     "horizontal_align": "left",
#                     "columns": [
#                         {
#                             "tag": "column",
#                             "width": "weighted",
#                             "vertical_align": "top",
#                             "vertical_spacing": "8px",
#                             "background_style": "default",
#                             "elements": [
#                                 {
#                                     "tag": "button",
#                                     "text": {
#                                         "tag": "plain_text",
#                                         "content": ""
#                                     },
#                                     "type": "primary_text",
#                                     "complex_interaction": "true",
#                                     "width": "default",
#                                     "size": "medium",
#                                     "icon": {
#                                         "tag": "standard_icon",
#                                         "token": "add-bold_outlined"
#                                     },
#                                     "hover_tips": {
#                                         "tag": "plain_text",
#                                         "content": "新会话"
#                                     },
#                                     "value": {
#                                         "event_type": "new_chat"
#                                     }
#                                 }
#                             ],
#                             "weight": 5
#                         },
#                         {
#                             "tag": "column",
#                             "width": "weighted",
#                             "vertical_align": "top",
#                             "vertical_spacing": "8px",
#                             "background_style": "default",
#                             "elements": [],
#                             "weight": 1
#                         },
#                         {
#                             "tag": "column",
#                             "width": "weighted",
#                             "vertical_align": "top",
#                             "vertical_spacing": "8px",
#                             "background_style": "default",
#                             "elements": [],
#                             "weight": 1
#                         }
#                     ],
#                     "margin": "16px 0px 0px 0px"
#                 }
#             ]
#         },
#         "i18n_header": {}
#     }
#
#     lark_message_util.send_card_message(
#         receive_id="ou_9d42bb88ec8940baf3ad183755131881",
#         content=var_8_TRX_TRUE_AMOUNT
#     )
#     lark_message_util.send_card_message(
#         receive_id="ou_9d42bb88ec8940baf3ad183755131881",
#         content=var_8_TRX_PROFIT
#     )
#
# #get_crem_hanglv_merchant_31days_search_card("ou_079964d3b15f58fc330058a629b8ed41", "段超")
#
#
#
#
#
#
# def get_crem_hanglv_merchant_8days_product_search_card(open_id,nickname,customer_no):
#     num_day8_before_yesterday,num_day31_before_yesterday = get_previous_dates()
#     url = (envutils.getenv("CREM_ENDPOINT_PROD") +
#            '/threeParty/wrap/apis/agg/productline_pcd_sh8daystrx')
#     headers = {
#         'yuiassotoken': ssoutil.get_sso_credential(open_id),
#         'Content-Type': 'application/json',
#         'pageType': 'cemPortal'
#
#     }
#
#     data = {
#                 "tenant": "default",
#                 "procDefKey": "15a8350f65a303736ebe606e3d30e5beM5",
#                 "data": {
#                     "dmallReq": {
#                         "parameters": {
#                             "TRX_DATE": num_day8_before_yesterday,
#                             "TYPE": "全部",
#                             "PRODUCTTYPE": "会员,旗舰店,收单,航旅快捷",
#                             "SUPERIOR_NAME": nickname,
#                             "STAT_SALES_NAME": nickname,
#                             "STAT_DISPAYSIGNEDNAME": customer_no
#                         },
#                         "url": "productline_pcd_hl_zt_sh8daystrx",
#                         "version": "V1.0"
#                     }
#                 }
#             }
#
#
#
#
#
#     # 发出 POST 请求
#     response = requests.post(url, headers=headers, json=data, timeout=consts.request_time_out)
#
#     # 处理 API 响应数据
#     api_data = json.loads(response.text)
#     print("原始数据",api_data)
#
#     # 将利润转换为万元并格式化数据
#     formatted_data = [
#         {
#             "type": entry["PRODUCTTYPE"],
#             "trxDate": entry["TRX_DATE"],
#             "profit": round(float(entry["TRX_PROFIT"]) / 10000, 2)  # 将利润转换为万元并保留两位小数
#         }
#         for entry in api_data["data"]["data"]
#     ]
#
#     # 生成完整的数据
#     complete_data = [
#                         # 会员
#                         {"trxDate": entry["trxDate"], "type": "会员", "profit": entry["profit"]}
#                         for entry in formatted_data if entry["type"] == "会员"
#                     ] + [
#                         # 旗舰店
#                         {"trxDate": entry["trxDate"], "type": "旗舰店", "profit": entry["profit"]}
#                         for entry in formatted_data if entry["type"] == "旗舰店"
#                     ] + [
#                         # 航旅快捷
#                         {"trxDate": entry["trxDate"], "type": "航旅快捷", "profit": entry["profit"]}
#                         for entry in formatted_data if entry["type"] == "航旅快捷"
#                     ]
#
#     print("完整的数据格式是",complete_data)
#
#     var = {
#         "config": {},
#         "i18n_elements": {
#             "zh_cn": [
#                 {
#                     "tag": "chart",
#                     "chart_spec": {
#                         "type": "area",
#                         "title": {
#                             "text": "近8天产品表现"+"——毛利——"+customer_no
#                         },
#                         "data": {
#                             "values":
#                                 complete_data},  # 更新数据部分
#
#                         "xField": "trxDate",
#                         "yField": "profit",
#                         "seriesField": "type",
#                         "axes": [
#                             {
#                                 "orient": "left",
#                                 "title": {
#                                     "visible": "true",
#                                     "text": "单位（万）"
#                                 }
#                             }
#                         ],
#                         "legends": [
#                             {
#                                 "visible": "true",
#                                 "position": "middle",
#                                 "orient": "bottom"
#                             }
#                         ],
#                         "stack": "false",
#                         "areaStyle": {
#                             "fillOpacity": 0.5
#                         },
#                         "lineStyle": {
#                             "strokeWidth": 2
#                         }
#                     }
#                 },
#                 {
#                     "tag": "column_set",
#                     "flex_mode": "none",
#                     "background_style": "default",
#                     "horizontal_spacing": "0px",
#                     "horizontal_align": "left",
#                     "columns": [
#                         {
#                             "tag": "column",
#                             "width": "weighted",
#                             "vertical_align": "top",
#                             "vertical_spacing": "8px",
#                             "background_style": "default",
#                             "elements": [
#                                 {
#                                     "tag": "button",
#                                     "text": {
#                                         "tag": "plain_text",
#                                         "content": ""
#                                     },
#                                     "type": "primary_text",
#                                     "complex_interaction": "true",
#                                     "width": "default",
#                                     "size": "medium",
#                                     "icon": {
#                                         "tag": "standard_icon",
#                                         "token": "add-bold_outlined"
#                                     },
#                                     "hover_tips": {
#                                         "tag": "plain_text",
#                                         "content": "新会话"
#                                     },
#                                     "value": {
#                                         "event_type": "new_chat"
#                                     }
#                                 }
#                             ],
#                             "weight": 5
#                         },
#                         {
#                             "tag": "column",
#                             "width": "weighted",
#                             "vertical_align": "top",
#                             "vertical_spacing": "8px",
#                             "background_style": "default",
#                             "elements": [],
#                             "weight": 1
#                         },
#                         {
#                             "tag": "column",
#                             "width": "weighted",
#                             "vertical_align": "top",
#                             "vertical_spacing": "8px",
#                             "background_style": "default",
#                             "elements": [],
#                             "weight": 1
#                         }
#                     ],
#                     "margin": "16px 0px 0px 0px"
#                 }
#             ]
#         },
#         "i18n_header": {}
#     }
#
#     lark_message_util.send_card_message(
#         receive_id="ou_9d42bb88ec8940baf3ad183755131881",
#         content=var
#     )
#
#
# #get_crem_hanglv_merchant_8days_product_search_card("ou_9d42bb88ec8940baf3ad183755131881","段超")
#
# def get_crem_hanglv_merchant_31days_product_search_card(open_id,nickname,customer_no):
#     num_day8_before_yesterday,num_day31_before_yesterday = get_previous_dates()
#     url = (envutils.getenv("CREM_ENDPOINT_PROD") +
#            '/threeParty/wrap/apis/agg/productline_pcd_sh8daystrx')
#     headers = {
#         'yuiassotoken': ssoutil.get_sso_credential(open_id),
#         'Content-Type': 'application/json',
#         'pageType': 'cemPortal'
#
#     }
#
#     data = {
#                 "tenant": "default",
#                 "procDefKey": "15a8350f65a303736ebe606e3d30e5beM5",
#                 "data": {
#                     "dmallReq": {
#                         "parameters": {
#                             "TRX_DATE": num_day31_before_yesterday,
#                             "TYPE": "全部",
#                             "PRODUCTTYPE": "会员,旗舰店,收单,航旅快捷",
#                             "SUPERIOR_NAME": nickname,
#                             "STAT_SALES_NAME": nickname,
#                             "STAT_DISPAYSIGNEDNAME": customer_no
#                         },
#                         "url": "productline_pcd_hl_zt_sh8daystrx",
#                         "version": "V1.0"
#                     }
#                 }
#             }
#
#
#
#
#
#     # 发出 POST 请求
#     response = requests.post(url, headers=headers, json=data, timeout=consts.request_time_out)
#
#     # 处理 API 响应数据
#     api_data = json.loads(response.text)
#     print("原始数据",api_data)
#
#     # 将利润转换为万元并格式化数据
#     formatted_data = [
#         {
#             "type": entry["PRODUCTTYPE"],
#             "trxDate": entry["TRX_DATE"],
#             "profit": round(float(entry["TRX_PROFIT"]) / 10000, 2)  # 将利润转换为万元并保留两位小数
#         }
#         for entry in api_data["data"]["data"]
#     ]
#
#     # 生成完整的数据
#     complete_data = [
#                         # 会员
#                         {"trxDate": entry["trxDate"], "type": "会员", "profit": entry["profit"]}
#                         for entry in formatted_data if entry["type"] == "会员"
#                     ] + [
#                         # 旗舰店
#                         {"trxDate": entry["trxDate"], "type": "旗舰店", "profit": entry["profit"]}
#                         for entry in formatted_data if entry["type"] == "旗舰店"
#                     ] + [
#                         # 航旅快捷
#                         {"trxDate": entry["trxDate"], "type": "航旅快捷", "profit": entry["profit"]}
#                         for entry in formatted_data if entry["type"] == "航旅快捷"
#                     ]
#
#     print("完整的数据格式是",complete_data)
#
#     var = {
#         "config": {},
#         "i18n_elements": {
#             "zh_cn": [
#                 {
#                     "tag": "chart",
#                     "chart_spec": {
#                         "type": "area",
#                         "title": {
#                             "text": "近31天产品表现"+"——毛利——"+customer_no
#                         },
#                         "data": {
#                             "values":
#                                 complete_data},  # 更新数据部分
#
#                         "xField": "trxDate",
#                         "yField": "profit",
#                         "seriesField": "type",
#                         "axes": [
#                             {
#                                 "orient": "left",
#                                 "title": {
#                                     "visible": "true",
#                                     "text": "单位（万）"
#                                 }
#                             }
#                         ],
#                         "legends": [
#                             {
#                                 "visible": "true",
#                                 "position": "middle",
#                                 "orient": "bottom"
#                             }
#                         ],
#                         "stack": "false",
#                         "areaStyle": {
#                             "fillOpacity": 0.5
#                         },
#                         "lineStyle": {
#                             "strokeWidth": 2
#                         }
#                     }
#                 },
#                 {
#                     "tag": "column_set",
#                     "flex_mode": "none",
#                     "background_style": "default",
#                     "horizontal_spacing": "0px",
#                     "horizontal_align": "left",
#                     "columns": [
#                         {
#                             "tag": "column",
#                             "width": "weighted",
#                             "vertical_align": "top",
#                             "vertical_spacing": "8px",
#                             "background_style": "default",
#                             "elements": [
#                                 {
#                                     "tag": "button",
#                                     "text": {
#                                         "tag": "plain_text",
#                                         "content": ""
#                                     },
#                                     "type": "primary_text",
#                                     "complex_interaction": "true",
#                                     "width": "default",
#                                     "size": "medium",
#                                     "icon": {
#                                         "tag": "standard_icon",
#                                         "token": "add-bold_outlined"
#                                     },
#                                     "hover_tips": {
#                                         "tag": "plain_text",
#                                         "content": "新会话"
#                                     },
#                                     "value": {
#                                         "event_type": "new_chat"
#                                     }
#                                 }
#                             ],
#                             "weight": 5
#                         },
#                         {
#                             "tag": "column",
#                             "width": "weighted",
#                             "vertical_align": "top",
#                             "vertical_spacing": "8px",
#                             "background_style": "default",
#                             "elements": [],
#                             "weight": 1
#                         },
#                         {
#                             "tag": "column",
#                             "width": "weighted",
#                             "vertical_align": "top",
#                             "vertical_spacing": "8px",
#                             "background_style": "default",
#                             "elements": [],
#                             "weight": 1
#                         }
#                     ],
#                     "margin": "16px 0px 0px 0px"
#                 }
#             ]
#         },
#         "i18n_header": {}
#     }
#
#     lark_message_util.send_card_message(
#         receive_id="ou_9d42bb88ec8940baf3ad183755131881",
#         content=var
#     )
#
#
# #get_crem_hanglv_merchant_31days_product_search_card("ou_9d42bb88ec8940baf3ad183755131881","段超")

