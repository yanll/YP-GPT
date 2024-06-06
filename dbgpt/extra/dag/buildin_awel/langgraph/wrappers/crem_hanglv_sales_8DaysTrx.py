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

    return num_day8_before_yesterday


def get_crem_hanglv_sales_8DaysTrx_card(open_id,nickname):
    trx_day = get_previous_dates()
    url = (envutils.getenv("CREM_ENDPOINT_PROD") +
           '/aggScript/wrap/apis/receive/handleApplicationMarketplace/saleXDayTrend')
    headers = {
        'yuiassotoken': ssoutil.get_sso_credential(open_id),
        'Content-Type': 'application/json',

    }

    data = {
            "parameters": {
                "TYPE": "航司,渠道,酒旅出行",
                "SCALE_TYPE": "DAY",
                "TRX_DATE": trx_day,
                "STAT_SALES_NAME": nickname
            },
            "strategyKey": "saleOrdinaryApplicationMarketExecutor"
              }





    # 发出 POST 请求
    response = requests.post(url, headers=headers, json=data, timeout=consts.request_time_out)

    # 处理 API 响应数据
    api_data = json.loads(response.text)

    # 将利润转换为万元并格式化数据
    formatted_data = [
        {
            "trxDate": entry["trxDate"],
            "type": entry["type"],
            "profit": round(entry["profit"] / 10000, 2)  # 将利润转换为万元并保留四位小数
        }
        for entry in api_data["data"]["data"]
    ]

    # 生成完整的数据
    complete_data = [
                        # 航司数据
                        {"trxDate": entry["trxDate"], "type": "航司", "profit": entry["profit"]}
                        for entry in formatted_data if entry["type"] == "航司"
                    ] + [
                        # 渠道数据
                        {"trxDate": entry["trxDate"], "type": "渠道", "profit": entry["profit"]}
                        for entry in formatted_data if entry["type"] == "渠道"
                    ] + [
                        # 酒旅出行数据
                        {"trxDate": entry["trxDate"], "type": "酒旅出行", "profit": entry["profit"]}
                        for entry in formatted_data if entry["type"] == "酒旅出行"
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
                            "text": "近8天毛利情况"
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
                                    "text": "单位（万元）"
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
                }
            ]
        },
        "i18n_header": {}
    }

    lark_message_util.send_card_message(
        receive_id=open_id,
        content=var
    )





# get_crem_hanglv_sales_8DaysTrx_card("ou_079964d3b15f58fc330058a629b8ed41","段超")



def get_crem_hanglv_boos_8DaysTrx_card(open_id,nickname):
    trx_day = get_previous_dates()
    url = (envutils.getenv("CREM_ENDPOINT_PROD") +
           '/aggScript/wrap/apis/receive/handleApplicationMarketplace/saleXDayTrend')
    headers = {
        'yuiassotoken': ssoutil.get_sso_credential(open_id),
        'Content-Type': 'application/json',
        'pageType': 'cemPortal',

    }

    data = {
        "parameters": {
            "TYPE": "航司",
            "SCALE_TYPE": "DAY",
            "TRX_DATE": trx_day,
            "SUPERIOR_NAME": nickname
        },
        "strategyKey": "saleOrdinaryApplicationMarketExecutor"
    }


    # 发出 POST 请求
    response = requests.post(url, headers=headers, json=data, timeout=consts.request_time_out)

    # 处理 API 响应数据
    api_data = json.loads(response.text)
    print("原本的数据是",api_data)

    # 将利润转换为万元并格式化数据
    formatted_data = [
        {
            "trxDate": entry["trxDate"],
            "type": entry["type"],
            "profit": round(entry["profit"] / 10000, 2)  # 将利润转换为万元并保留四位小数
        }
        for entry in api_data["data"]["data"]
    ]

    # 生成完整的数据
    complete_data = [
                        # 航司数据
                        {"trxDate": entry["trxDate"], "type": "航司", "profit": entry["profit"]}
                        for entry in formatted_data if entry["type"] == "航司"
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
                            "text": "近8天毛利情况"
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
                                    "text": "单位（万元）"
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

# get_crem_hanglv_boos_8DaysTrx_card("ou_dd02cefd5b0d267928a80bedfd3d2100","宋岩")




