import logging

import requests
import json
from datetime import datetime, timedelta

from sqlalchemy import null

from dbgpt.util import envutils
from dbgpt.util.lark import larkutil, ssoutil

global nickname
# open_id = "ou_9d42bb88ec8940baf3ad183755131881"
def sales_board_display(open_id):
    global nickname
    url = envutils.getenv("CREM_ENDPOINT_PROD") + '/crmCustomer/getSuperiorAndSubordinate'

    headers = {
        'yuiassotoken': ssoutil.get_sso_credential(open_id),
        'pageType': 'cemPortal',

    }

    try:
        userinfo = larkutil.select_userinfo(open_id=open_id)
        if userinfo and "name" in userinfo:
            nickname = userinfo["name"] + " "
            print("用户的姓名是", nickname)
    except Exception as e:
        logging.warning("用户姓名解析异常：", open_id)


    data = {
        "requestParams": "SUPERIOR_NAME",
        "targetParams": "SALES_NAME",
        "userName": nickname
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        if 'data' in result and 'userType' in result['data']:
            user_type_value = result['data']['userType']
            print("成功获取销售看板数据！")
            print("数据userType对应的值为：", user_type_value)
            return user_type_value

        else:
            print("未找到数据用户类型信息")
    else:
        print("请求失败：", response.status_code)





def industry_line(open_id=None):
    url = envutils.getenv("CREM_ENDPOINT_PROD") + '/common/treeDictionary'

    headers = {
        'yuiassotoken': ssoutil.get_sso_credential(open_id),
        'pageType': 'cemPortal',

    }
    data = {
        "type": "49"
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            # 从返回结果中获取类型名并直接输出
            typename = result['data'][0]['typename']
            print("数据typename的值为：", typename)
            return typename
        else:
            print("请求失败：", response.status_code)
    except Exception as e:
        print("请求时出现异常：", e)

def get_previous_dates():
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    day7_before_yesterday = today - timedelta(days=7)
    day_before_yesterday = today - timedelta(days=2)
    weekly_before_today = yesterday - timedelta(days=7)

    return yesterday.strftime('%Y-%m-%d'), day_before_yesterday.strftime('%Y-%m-%d'), day7_before_yesterday.strftime('%Y-%m-%d'), weekly_before_today.strftime('%Y-%m-%d')

def maolicase(trx_date, open_id):
    global nickname
    nickname = ""

    try:
        userinfo = larkutil.select_userinfo(open_id=open_id)
        if userinfo and "name" in userinfo:
            nickname = userinfo["name"] + " "
            print("用户的姓名是", nickname)
    except Exception as e:
        logging.warning("用户姓名解析异常：", open_id)

    #user_type_value = 2
    #typename = "金融行业线"
    user_type_value = sales_board_display(open_id)
    typename = industry_line(open_id)
    url_map = {
        "航旅事业部": {
            0: envutils.getenv(
                "CREM_ENDPOINT_APP") + "/mobile/aggScript/wrap/apis/receive/handleApplicationMarketplace/hv_jf_day_summary_situate_one",
            1: envutils.getenv(
                "CREM_ENDPOINT_APP") + "/mobile/aggScript/wrap/apis/receive/handleApplicationMarketplace/hv_jf_day_summary_situate_one",
            2: envutils.getenv(
                "CREM_ENDPOINT_APP") + "/mobile/aggScript/wrap/apis/receive/handleApplicationMarketplace/hv_jf_day_summary_situate_one",
        },
        "跨境行业线": {
            0: envutils.getenv(
                "CREM_ENDPOINT_APP") + "/mobile/threeParty/wrap/apis/agg/package_crem_kjxm_jyfx_ydd_hzqk",
            1: envutils.getenv("CREM_ENDPOINT_APP") + "/mobile/threeParty/wrap/apis/agg/crem_salesmanage_kj_ydd_hzqk",
            2: envutils.getenv(
                "CREM_ENDPOINT_APP") + "/mobile/threeParty/wrap/apis/agg/package_crem_kjxm_jyfx_ydd_hzqk",
        },
        "金融行业线": {
            0: envutils.getenv(
                "CREM_ENDPOINT_APP") + "/mobile/threeParty/wrap/apis/agg/package_salesmanagereport_ydd_hzqk",
            1: envutils.getenv(
                "CREM_ENDPOINT_APP") + "/mobile/threeParty/wrap/apis/agg/package_salesmanagereport_ydd_hzqk",
            2: envutils.getenv(
                "CREM_ENDPOINT_APP") + "/mobile/threeParty/wrap/apis/agg/package_salesmanagereport_ydd_hzqk",
        },
        "大零售行业线": {
            0: envutils.getenv("CREM_ENDPOINT_APP") + "/mobile/threeParty/wrap/apis/agg/package_salesmanagereport_ydd_hzqk",
            1: envutils.getenv("CREM_ENDPOINT_APP") + "/mobile/threeParty/wrap/apis/agg/package_salesreport_ydd_hzqk",
            2: envutils.getenv("CREM_ENDPOINT_APP") + "/mobile/threeParty/wrap/apis/agg/package_salesmanagereport_ydd_hzqk",
        }
    }
    # url_map = {
    #     "航旅事业部": {
    #         0: envutils.getenv("CREM_ENDPOINT_APP") + "/mobile/aggScript/wrap/apis/receive/handleApplicationMarketplace/hv_jf_day_summary_situate_one",
    #         1: envutils.getenv("CREM_ENDPOINT_APP") + "/mobile/aggScript/wrap/apis/receive/handleApplicationMarketplace/hv_jf_day_summary_situate_one",
    #         2: envutils.getenv("CREM_ENDPOINT_APP") + "/mobile/aggScript/wrap/apis/receive/handleApplicationMarketplace/hv_jf_day_summary_situate_one",
    #
    #     },
    #     "跨境行业线": {
    #         0: envutils.getenv("CREM_ENDPOINT_APP") + "/mobile/threeParty/wrap/apis/agg/package_crem_kjxm_jyfx_ydd_hzqk",
    #         1: envutils.getenv("CREM_ENDPOINT_APP") + "/mobile/threeParty/wrap/apis/agg/crem_salesmanage_kj_ydd_hzqk",
    #         2: envutils.getenv("CREM_ENDPOINT_APP") + "/mobile/threeParty/wrap/apis/agg/package_crem_kjxm_jyfx_ydd_hzqk",
    #
    #     },
    #     "金融行业线": {
    #         0: envutils.getenv("CREM_ENDPOINT_APP") + "/mobile/threeParty/wrap/apis/agg/package_salesmanagereport_ydd_hzqk",
    #         1: envutils.getenv("CREM_ENDPOINT_APP") + "/mobile/threeParty/wrap/apis/agg/package_salesmanagereport_ydd_hzqk",
    #         2: envutils.getenv("CREM_ENDPOINT_APP") + "/mobile/threeParty/wrap/apis/agg/package_salesmanagereport_ydd_hzqk",
    #
    #     },
    #     "大零售行业线": {
    #         0: envutils.getenv("CREM_ENDPOINT_APP") + "/mobile/threeParty/wrap/apis/agg/package_salesmanagereport_ydd_hzqk",
    #         1: envutils.getenv("CREM_ENDPOINT_APP") + "/mobile/threeParty/wrap/apis/agg/package_salesreport_ydd_hzqk",
    #         2: envutils.getenv("CREM_ENDPOINT_APP") + "/mobile/threeParty/wrap/apis/agg/package_salesmanagereport_ydd_hzqk",
    #     }
    # }

    # url_map = {
    #     "航旅事业部": envutils.getenv("CREM_ENDPOINT_APP") + '/mobile/aggScript/wrap/apis/receive/handleApplicationMarketplace/hv_jf_day_summary_situate_one',
    #     "跨境行业线": envutils.getenv("CREM_ENDPOINT_APP") + '/mobile/threeParty/wrap/apis/agg/package_crem_kjxm_jyfx_ydd_hzqk',
    #     "金融行业线": envutils.getenv("CREM_ENDPOINT_APP") + '/mobile/threeParty/wrap/apis/agg/package_salesmanagereport_ydd_hzqk',
    #     "大零售行业线": envutils.getenv("CREM_ENDPOINT_APP") + '/mobile/threeParty/wrap/apis/agg/package_salesreport_ydd_hzqk'
    #
    # }

    data_map = {
        "航旅事业部": {
            0: {
                "parameters": {
                    "TYPE": "航司",
                    "SCALE_TYPE": "DAY",
                    "TRX_DATE": trx_date,
                    "SUPERIOR_NAME": "宋岩",
                    "STAT_SALES_NAME": None
                },
                "strategyKey": "saleOrdinaryApplicationMarketExecutor"
            },
            1: {
                "parameters": {
                    "TYPE": "航司,渠道,酒旅出行",
                    "SCALE_TYPE": "DAY",
                    "TRX_DATE": trx_date,
                    "STAT_SALES_NAME": "段超"
                },
                "strategyKey": "saleOrdinaryApplicationMarketExecutor"
            },
            2: {
                "parameters": {
                    "TYPE": "航司,渠道,酒旅出行",
                    "SCALE_TYPE": "DAY",
                    "TRX_DATE": trx_date,
                    "STAT_SALES_NAME": nickname
                },
                "strategyKey": "saleOrdinaryApplicationMarketExecutor"
            }
        },
        "跨境行业线": {
            0: {
                "tenant": "default",
                "procDefKey": "15a8350f65a303736ebe606e3d30e5beM2",
                "data": {
                    "dmallReq": {
                        "parameters": {
                            "TRX_DATE": trx_date,
                            "LAST_DATE": "2024-04-16,2024-04-16"
                        },
                        "url": "package_crem_kjxm_jyfx_ydd_hzqk",
                        "version": "V1.0"
                    }
                }
            },
            1: {
                "tenant": "default",
                "procDefKey": "dmallGeneral",
                "data": {
                    "dmallReq": {
                        "parameters": {
                            "TRX_DATE": trx_date,
                            "MERCHANT_SALESNAME": "柳永亮"
                        },
                        "url": "crem_salesmanage_kj_ydd_hzqk",
                        "version": "V1.0"
                    }
                }
            },
            2: {
                "tenant": "default",
                "procDefKey": "dmallGeneral",
                "data": {
                    "dmallReq": {
                        "parameters": {
                            "TRX_DATE": trx_date,
                            "MERCHANT_SALESNAME": nickname
                        },
                        "url": "crem_salesmanage_kj_ydd_hzqk",
                        "version": "V1.0"
                    }
                }
            }
        },
        "金融行业线": {
            0: {
                "tenant": "default",
                "procDefKey": "15a8350f65a303736ebe606e3d30e5beM3",
                "data": {
                    "dmallReq": {
                        "parameters": {
                            "TRX_DATE": trx_date,
                            "TYPE": "全部",
                            "SUPERIOR_NAME": "刘刚-1"
                        },
                        "url": "package_salesmanagereport_ydd_hzqk",
                        "version": "V1.0"
                    },
                    "LAST_DATE": "2024-04-01,2024-04-16"
                }
            },
            1: {
                "tenant": "default",
                "procDefKey": "15a8350f65a303736ebe606e3d30e5beM3",
                "data": {
                    "dmallReq": {
                        "parameters": {
                            "TRX_DATE": trx_date,
                            "TYPE": "全部",
                            "STAT_SALES_NAME": "王紫薇",
                            "SUPERIOR_NAME": "王紫薇"
                        },
                        "url": "package_salesmanagereport_ydd_hzqk",
                        "version": "V1.0"
                    },
                    "LAST_DATE": "2024-04-16,2024-04-16"
                }
            },
            2: {
                "tenant": "default",
                "procDefKey": "15a8350f65a303736ebe606e3d30e5beM3",
                "data": {
                    "dmallReq": {
                        "parameters": {
                            "TRX_DATE": trx_date,
                            "TYPE": "全部",
                            "SUPERIOR_NAME": nickname
                        },
                        "url": "package_salesmanagereport_ydd_hzqk",
                        "version": "V1.0"
                    },
                    "LAST_DATE": "2024-04-01,2024-04-16"
                }
            }
        },
        "大零售行业线": {
            0: {
                "tenant": "default",
                "procDefKey": "15a8350f65a303736ebe606e3d30e5beM3",
                "data": {
                    "dmallReq": {
                        "parameters": {
                            "TRX_DATE": trx_date,
                            "TYPE": "全部",
                            "SUPERIOR_NAME": "田愉快"
                        },
                        "url": "package_salesmanagereport_ydd_hzqk",
                        "version": "V1.0"
                    },
                    "LAST_DATE": "2024-04-01,2024-04-17",
                    "team": "全部"
                }
            },
            1: {
                "tenant": "default",
                "procDefKey": "15a8350f65a303736ebe606e3d30e5beM3",
                "data": {
                    "dmallReq": {
                        "parameters": {
                            "TRX_DATE": trx_date,
                            "TYPE": "全部",
                            "STAT_SALES_NAME": "刘鹏程"
                        },
                        "url": "package_salesreport_ydd_hzqk",
                        "version": "V1.0"
                    },
                    "LAST_DATE": "2024-04-01,2024-04-17"
                }
            },
            2: {
                "tenant": "default",
                "procDefKey": "15a8350f65a303736ebe606e3d30e5beM3",
                "data": {
                    "dmallReq": {
                        "parameters": {
                            "TRX_DATE": trx_date,
                            "TYPE": "全部",
                            "SUPERIOR_NAME": nickname
                        },
                        "url": "package_salesmanagereport_ydd_hzqk",
                        "version": "V1.0"
                    },
                    "LAST_DATE": "2024-04-01,2024-04-17",
                    "team": "全部"
                }
            }
        }
    }

    # 根据typename选择url和data
    url = url_map.get(typename, {}).get(user_type_value, "")
    data = data_map.get(typename, {}).get(user_type_value, {})

    headers = {
        'yuiassotoken': ssoutil.get_sso_credential(open_id),
        'pageType': 'cemPortal',
        'Content-Type': 'application/json',
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    # 检查响应状态码
    if response.status_code == 200:
        try:
            # 尝试解析JSON数据
            json_data = response.json()
            print(json_data)
            # 航旅处理
            if "data" in json_data and isinstance(json_data["data"], dict):
                data = json_data["data"]
                if "TRX_PROFIT" in data and data["TRX_PROFIT"] is not None:
                    trx_profit = float(data["TRX_PROFIT"])
                    print("航旅销售的值是", trx_profit)
                    return trx_profit

            # 跨境处理
            if "data" in json_data and isinstance(json_data["data"], dict) and "data" in json_data[
                "data"] and isinstance(
                    json_data["data"]["data"], list):
                data_list = json_data["data"]["data"]
                if len(data_list) > 0 and "TRX_PROFIT" in data_list[0] and data_list[0]["TRX_PROFIT"] is not None:
                    trx_profit = float(data_list[0]["TRX_PROFIT"])
                    print("跨境销售的值是", trx_profit)
                    return trx_profit

            # 金融处理
            if "data" in json_data and isinstance(json_data["data"], dict):
                data = json_data["data"]
                # if "chain" in data and isinstance(data["chain"], list) and len(data["chain"]) > 0 and "TRX_PROFIT" in \
                #         data["chain"][0] and data["chain"][0]["TRX_PROFIT"] is not None:
                #     trx_profit = float(data["chain"][0]["TRX_PROFIT"])
                #     print("金融链销售的值是", trx_profit)
                #     return trx_profit
                if "data" in data and isinstance(data["data"], list) and len(data["data"]) > 0 and "TRX_PROFIT" in \
                        data["data"][
                            0] and data["data"][0]["TRX_PROFIT"] is not None:
                    trx_profit = float(data["data"][0]["TRX_PROFIT"])
                    print("金融数据销售的值是", trx_profit)
                    return trx_profit

            # 大零售处理
            if "data" in json_data and isinstance(json_data["data"], dict):
                data = json_data["data"]
                # if "chain" in data and isinstance(data["chain"], list) and len(data["chain"]) > 0 and "TRX_PROFIT" in \
                #         data["chain"][0] and data["chain"][0]["TRX_PROFIT"] is not None:
                #     trx_profit = float(data["chain"][0]["TRX_PROFIT"])
                #     print("大零售销售的值是", trx_profit)
                #     return trx_profit
                if "data" in data and isinstance(data["data"], list) and len(data["data"]) > 0 and "TRX_PROFIT" in \
                        data["data"][
                            0] and data["data"][0]["TRX_PROFIT"] is not None:
                    trx_profit = float(data["data"][0]["TRX_PROFIT"])
                    print("大零售数据销售的值是", trx_profit)
                    return trx_profit




            # 返回提示消息
            return {"error": "你不是销售"}
        except json.decoder.JSONDecodeError:
            logging.error("无法解析JSON数据:", response.text)
            return {"error": "无法解析JSON数据"}
    else:
        logging.error("请求失败:", response.status_code)
        return {"error": "请求失败"}


def format_profit(profit):
    formatted_profit = f"{profit / 10000:.2f}"  # 转换为万元并保留两位小数
    formatted_profit = format(float(formatted_profit), ',')  # 添加千分位
    return formatted_profit



def shujuqingk(open_id):
    # 获取昨天和前天的日期
    global yesterday_change_rate_formatted
    yesterday, day_before_yesterday, day7_before_yesterday, weekly_before_today = get_previous_dates()
    trx_date_yesterday = f"{yesterday},{yesterday}"
    trx_date_day_before_yesterday = f"{day_before_yesterday},{day_before_yesterday}"
    trx_date_day7_before_yesterday = f"{day7_before_yesterday},{yesterday}"
    trx_date_weekly_before_today = f"{weekly_before_today},{weekly_before_today}"

    # 调用函数并获取结果
    result_yesterday = maolicase(trx_date_yesterday, open_id)
    result_day_before_yesterday = maolicase(trx_date_day_before_yesterday, open_id)
    result_day7_before_yesterday = maolicase(trx_date_day7_before_yesterday, open_id)
    result_weekly_before_today = maolicase(trx_date_weekly_before_today, open_id)

    # 检查是否进行了非正常查询
    if isinstance(result_yesterday, dict) and 'error' in result_yesterday or \
       isinstance(result_day_before_yesterday, dict) and 'error' in result_day_before_yesterday or \
       isinstance(result_day7_before_yesterday, dict) and 'error' in result_day7_before_yesterday or \
       isinstance(result_weekly_before_today, dict) and 'error' in result_weekly_before_today:
        profit_yesterday = "数据为空，你不是销售"
        profit_day_before_yesterday = "数据为空，你不是销售"
        profit_day7_before_yesterday = "数据为空，你不是销售"
        average_day7_before_yesterday = "数据为空，你不是销售"
        yesterday_change_rate_formatted = "数据为空，你不是销售"
        weekly_change_rate_formatted = "数据为空，你不是销售"
    else:
        # 提取毛利数据并格式化
        profit_yesterday = format_profit(result_yesterday)
        profit_day_before_yesterday = format_profit(result_day_before_yesterday)
        profit_day7_before_yesterday = format_profit(result_day7_before_yesterday)

        # 计算前7天平均每日毛利
        average_day7_before_yesterday = format_profit(result_day7_before_yesterday / 7)

        # 计算昨天相对于前天的同比变化率
        if result_day_before_yesterday != 0:
            yesterday_change_rate = ((result_yesterday - result_day_before_yesterday) / result_day_before_yesterday) * 100
            yesterday_change_rate_formatted = "{:.2f}%".format(yesterday_change_rate)
        else:
            yesterday_change_rate_formatted = "数据为空"

        # 计算上周同一时间的毛利变化率
        if result_weekly_before_today != 0:
            weekly_change_rate = ((result_yesterday - result_weekly_before_today) / result_weekly_before_today) * 100
            weekly_change_rate_formatted = "{:.2f}%".format(weekly_change_rate)
        else:
            weekly_change_rate_formatted = "数据为空"

    # 返回数据字典
    return {
        '昨天的毛利': profit_yesterday,
        '前天的毛利': profit_day_before_yesterday,
        '昨天相对于前天的同比变化率': yesterday_change_rate_formatted,
        '上周同一时间的毛利变化率': weekly_change_rate_formatted,
        '前7天的毛利总额': profit_day7_before_yesterday,
        '前7天的平均毛利': average_day7_before_yesterday
    }

# 调用示例
# result = shujuqingk(open_id='your_open_id')
# print(result)

# def format_profit(profit):
#     formatted_profit = f"{profit / 10000:.2f}"  # 转换为万元并保留两位小数
#     formatted_profit = format(float(formatted_profit), ',')  # 添加千分位
#     return formatted_profit
#
#
#
# def shujuqingk(open_id):
#
#     # 获取昨天和前天的日期
#     global yesterday_change_rate_formatted
#     yesterday, day_before_yesterday, day7_before_yesterday, weekly_before_today = get_previous_dates()
#     trx_date_yesterday = f"{yesterday},{yesterday}"
#     trx_date_day_before_yesterday = f"{day_before_yesterday},{day_before_yesterday}"
#     trx_date_day7_before_yesterday = f"{day7_before_yesterday},{yesterday}"
#     trx_date_weekly_before_today = f"{weekly_before_today},{weekly_before_today}"
#
#     # 调用函数并获取结果
#     result_yesterday = maolicase(trx_date_yesterday,open_id)
#     result_day_before_yesterday = maolicase(trx_date_day_before_yesterday,open_id)
#     result_day7_before_yesterday = maolicase(trx_date_day7_before_yesterday,open_id)
#     result_weekly_before_today = maolicase(trx_date_weekly_before_today,open_id)
#
#     # 检查是否进行了非正常查询
#     if 'error' in result_yesterday or 'error' in result_day_before_yesterday or 'error' in result_day7_before_yesterday or 'error' in result_weekly_before_today:
#         # 如果进行了非正常查询，则返回所有毛利字段的值为"数据为空"
#         profit_yesterday = "数据为空"
#         profit_day_before_yesterday = "数据为空"
#         profit_day7_before_yesterday = "数据为空"
#         average_day7_before_yesterday = "数据为空"
#         yesterday_change_rate = "数据为空"
#         yesterday_change_rate_formatted = "数据为空"
#         weekly_change_rate_formatted = "数据为空"
#     else:
#         # 提取毛利数据并格式化
#         profit_yesterday = format_profit(result_yesterday)
#         profit_day_before_yesterday = format_profit(result_day_before_yesterday)
#         profit_day7_before_yesterday = format_profit(result_day7_before_yesterday)
#
#         # 计算前7天平均每日毛利
#         if result_day7_before_yesterday['data']['TRX_PROFIT'] is None:
#             average_day7_before_yesterday = "数据为空"
#         else:
#             average_day7_before_yesterday = format_profit(result_day7_before_yesterday['data']['TRX_PROFIT'] / 7)
#
#         # 计算昨天相对于前天的同比变化率
#         profit_yesterday_x = float(result_yesterday['data']['TRX_PROFIT'])
#         profit_day_before_yesterday_x = float(result_day_before_yesterday['data']['TRX_PROFIT'])
#         yesterday_change_rate = ((profit_yesterday_x - profit_day_before_yesterday_x) / profit_day_before_yesterday_x) * 100
#         yesterday_change_rate_formatted = "{:.2f}%".format(yesterday_change_rate)
#         # 计算上周同一时间的毛利变化率
#         profit_weekly_before_today_x = float(result_weekly_before_today['data']['TRX_PROFIT'])
#         weekly_change_rate = ((profit_yesterday_x - profit_weekly_before_today_x) / profit_weekly_before_today_x) * 100
#         weekly_change_rate_formatted = "{:.2f}%".format(weekly_change_rate)
#
#     # 返回数据字典
#     return {
#         '昨天的毛利': profit_yesterday,
#         '前天的毛利': profit_day_before_yesterday,
#         '昨天相对于前天的同比变化率': yesterday_change_rate_formatted,
#         '上周同一时间的毛利变化率': weekly_change_rate_formatted,
#         '前7天的毛利总额': profit_day7_before_yesterday,
#         '前7天的平均毛利': average_day7_before_yesterday
#     }
#
