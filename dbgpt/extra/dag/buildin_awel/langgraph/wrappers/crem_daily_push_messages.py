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

    # 增加日志信息
    logging.info(f"请求的URL: {url}")
    logging.info(f"请求的open_id: {open_id}")

    headers = {
        'yuiassotoken': ssoutil.get_sso_credential(open_id),
        'pageType': 'cemPortal',
    }

    logging.info(f"请求的headers: {headers}")

    try:
        userinfo = larkutil.select_userinfo(open_id=open_id)
        logging.info(f"获取的用户信息: {userinfo}")
        if userinfo and "name" in userinfo:
            nickname = str(userinfo["name"])
            print("用户的姓名是", nickname)

            if nickname.strip() == "高峰":
                nickname = "宋岩"
                user_type_value = 0
                return user_type_value
            if nickname.strip() == "苏杨生":
                nickname = "段超"

            print("使用的用户姓名是", nickname)
        else:
            nickname = "Unknown "
    except Exception as e:
        logging.warning(f"用户姓名解析异常：{e}")
        nickname = "Unknown "

    data = {
        "requestParams": "SUPERIOR_NAME",
        "targetParams": "SALES_NAME",
        "userName": nickname
    }

    logging.info(f"请求的数据: {data}")

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # 检查HTTP请求是否成功
        result = response.json()
        logging.info(f"响应的JSON数据: {result}")

        # 检查'result'是否为None
        if result is None:
            logging.error("响应的JSON数据为空")
            return 2

        if 'data' in result and isinstance(result['data'], dict) and 'userType' in result['data']:
            user_type_value = result['data']['userType']
            print("成功获取销售看板数据！")
            print("数据userType对应的值为：", user_type_value)
        else:
            print("未找到数据用户类型信息")
            user_type_value = 2
    except requests.exceptions.RequestException as e:
        logging.error(f"请求失败：{e}")
        user_type_value = 2
    except ValueError as e:
        logging.error(f"响应JSON解析失败：{e}")
        user_type_value = 2
    except KeyError as e:
        logging.error(f"响应中缺少预期的键：{e}")
        user_type_value = 2
    except TypeError as e:
        logging.error(f"类型错误：{e}")
        user_type_value = 2
    except Exception as e:
        logging.error(f"未知错误：{e}")
        user_type_value = 2

    return user_type_value



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
    today = datetime.now()  #今天
    yesterday = today - timedelta(days=1) #昨天
    day_before_yesterday = today - timedelta(days=2)  # 前天
    day7_before_yesterday = today - timedelta(days=7) #今天是周一，那就是上周的周一     今天减去7天  8号是周一（今天）减去7天等于1号，也就是上周周一
    print("上周的今天",day7_before_yesterday)
    weekly_before_today = yesterday - timedelta(days=7) #上上周周日
    print("上周的前天+++++++",weekly_before_today)

    return yesterday.strftime('%Y-%m-%d'), day_before_yesterday.strftime('%Y-%m-%d'), day7_before_yesterday.strftime('%Y-%m-%d'), weekly_before_today.strftime('%Y-%m-%d')

def maolicase(trx_date, open_id):
    global nickname
    nickname = ""

    try:
        userinfo = larkutil.select_userinfo(open_id=open_id)
        if userinfo and "name" in userinfo:
            nickname = str(userinfo["name"])
            print("用户的姓名是", nickname)

            if (nickname.strip() == "高峰") or (nickname.strip() == "苏杨生"):
                nickname = "宋岩"

            print("使用的用户姓名是", nickname)
    except Exception as e:
        logging.warning("用户姓名解析异常：", open_id)


    #user_type_value = 2
    #typename = "金融行业线"
    user_type_value = sales_board_display(open_id)
    typename = industry_line(open_id)

    if user_type_value is None or typename is None:
        jieguo = [user_type_value, typename]
        print("选项集合", jieguo)
        return {"error": "你不是销售"}  # 返回错误消息
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
            1: envutils.getenv(
                "CREM_ENDPOINT_APP") + "/mobile/threeParty/wrap/apis/agg/crem_salesmanage_kj_ydd_hzqk",
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
            0: envutils.getenv(
                "CREM_ENDPOINT_APP") + "/mobile/threeParty/wrap/apis/agg/package_salesmanagereport_ydd_hzqk",
            1: envutils.getenv(
                "CREM_ENDPOINT_APP") + "/mobile/threeParty/wrap/apis/agg/package_salesreport_ydd_hzqk",
            2: envutils.getenv(
                "CREM_ENDPOINT_APP") + "/mobile/threeParty/wrap/apis/agg/package_salesmanagereport_ydd_hzqk",
        },
        "政务行业线": {
            0: envutils.getenv(
                "CREM_ENDPOINT_APP") + "/mobile/threeParty/wrap/apis/agg/package_salesmanagereport_ydd_hzqk",
            1: envutils.getenv(
                "CREM_ENDPOINT_APP") + "/mobile/threeParty/wrap/apis/agg/package_salesreport_ydd_hzqk",
            2: envutils.getenv(
                "CREM_ENDPOINT_APP") + "/mobile/threeParty/wrap/apis/agg/package_salesmanagereport_ydd_hzqk",
        }
    }

    data_map = {
        "航旅事业部": {
            0: {
                "parameters": {
                    "TYPE": "航司",
                    "SCALE_TYPE": "DAY",
                    "TRX_DATE": trx_date,
                    "SUPERIOR_NAME": nickname,
                    "STAT_SALES_NAME": None
                },
                "strategyKey": "saleOrdinaryApplicationMarketExecutor"
            },
            1: {
                "parameters": {
                    "TYPE": "航司,渠道,酒旅出行",
                    "SCALE_TYPE": "DAY",
                    "TRX_DATE": trx_date,
                    "STAT_SALES_NAME": nickname
                },
                "strategyKey": "saleOrdinaryApplicationMarketExecutor"
            },
            2: {
                "parameters": {
                    "TYPE": "航司",
                    "SCALE_TYPE": "DAY",
                    "TRX_DATE": trx_date,
                    "SUPERIOR_NAME": nickname,
                    "STAT_SALES_NAME": None
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
        },
        "政务行业线": {
            0: {
                "tenant": "default",
                "procDefKey": "15a8350f65a303736ebe606e3d30e5beM3",
                "data": {
                    "dmallReq": {
                        "parameters": {
                            "TRX_DATE": trx_date,
                            "STAT_SALES_NAME": nickname
                        },
                        "url": "package_salesreport_ydd_hzqk",
                        "version": "V1.0"
                    },
                    "LAST_DATE": "2024-04-01,2024-04-18"
                }
            },
            1: {
                "tenant": "default",
                "procDefKey": "15a8350f65a303736ebe606e3d30e5beM3",
                "data": {
                    "dmallReq": {
                        "parameters": {
                            "TRX_DATE": trx_date,
                            "STAT_SALES_NAME": "黄小翠"
                        },
                        "url": "package_salesreport_ydd_hzqk",
                        "version": "V1.0"
                    },
                    "LAST_DATE": "2024-04-01,2024-04-18"
                }
            },
            2: {
                "tenant": "default",
                "procDefKey": "15a8350f65a303736ebe606e3d30e5beM3",
                "data": {
                    "dmallReq": {
                        "parameters": {
                            "TRX_DATE": trx_date,
                            "STAT_SALES_NAME": nickname
                        },
                        "url": "package_salesreport_ydd_hzqk",
                        "version": "V1.0"
                    },
                    "LAST_DATE": "2024-04-01,2024-04-18"
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
    print("昨天的日期++++++++++++", trx_date_yesterday)
    trx_date_day_before_yesterday = f"{day_before_yesterday},{day_before_yesterday}"
    print("前天的日期++++++++++++", trx_date_day_before_yesterday)
    trx_date_day7_before_yesterday = f"{day7_before_yesterday},{yesterday}"
    print("前七天毛利++++++++++++",trx_date_day7_before_yesterday)
    trx_date_weekly_before_today = f"{weekly_before_today},{weekly_before_today}"
    print("上周同比前天的日期++++++++++++",trx_date_weekly_before_today)


    # 调用函数并获取结果
    result_yesterday = maolicase(trx_date_yesterday, open_id)  #昨天
    result_day_before_yesterday = maolicase(trx_date_day_before_yesterday, open_id)#前天
    result_day7_before_yesterday = maolicase(trx_date_day7_before_yesterday, open_id)
    result_weekly_before_today = maolicase(trx_date_weekly_before_today, open_id)

    # 检查是否进行了非正常查询
    if isinstance(result_yesterday, dict) and 'error' in result_yesterday or \
       isinstance(result_day_before_yesterday, dict) and 'error' in result_day_before_yesterday or \
       isinstance(result_day7_before_yesterday, dict) and 'error' in result_day7_before_yesterday or \
       isinstance(result_weekly_before_today, dict) and 'error' in result_weekly_before_today:
        profit_yesterday = "数据为空，你不是销售"  #昨天
        profit_day_before_yesterday = "数据为空，你不是销售"  #前天
        profit_day7_before_yesterday = "数据为空，你不是销售"  #昨日同比
        average_day7_before_yesterday = "数据为空，你不是销售" # 前七天平均
        yesterday_change_rate_formatted = "数据为空，你不是销售"
        weekly_change_rate_formatted = "数据为空，你不是销售"
        yesterday777_change_rate_formatted = "数据为空，你不是销售"
    else:
        # 提取毛利数据并格式化
        profit_yesterday = format_profit(result_yesterday)
        profit_day_before_yesterday = format_profit(result_day_before_yesterday)
        profit_day7_before_yesterday = format_profit(result_day7_before_yesterday)

        # 计算前7天平均每日毛利
        average_day7_before_yesterday = format_profit(result_day7_before_yesterday / 7)
        average_day7_before_yesterday_before = result_day7_before_yesterday / 7

        # 计算昨天相对于前天的同比变化率
        if result_day_before_yesterday != 0:
            yesterday_change_rate = ((result_yesterday - result_day_before_yesterday) / result_day_before_yesterday) * 100
            yesterday_change_rate_formatted = "{:.2f}%".format(yesterday_change_rate)
        else:
            yesterday_change_rate_formatted = "数据为空"

        # 计算上周同一时间的毛利变化率
        if result_yesterday != 0:
            weekly_change_rate = ((result_yesterday - result_weekly_before_today) / result_weekly_before_today) * 100
            print("昨天的毛利++++++++++++",result_yesterday)
            print("上周同比昨天的毛利++++++++++++",result_weekly_before_today)
            weekly_change_rate_formatted = "{:.2f}%".format(weekly_change_rate)
        else:
            weekly_change_rate_formatted = "数据为空"

        # 计算昨日同比7日平均变化率
        if average_day7_before_yesterday_before != 0:
            yesterday777_change_rate = ((result_yesterday - average_day7_before_yesterday_before) / average_day7_before_yesterday_before) * 100
            print("昨天的毛利++++++++++++",result_yesterday)
            print("七日平均毛利++++++++++++",average_day7_before_yesterday_before)
            yesterday777_change_rate_formatted = "{:.2f}%".format(yesterday777_change_rate)
        else:
            yesterday777_change_rate_formatted = "数据为空"

    # 返回数据字典
    return {
        '昨天的毛利': profit_yesterday,
        '前天的毛利': profit_day_before_yesterday,
        '昨天相对于前天的同比变化率': yesterday_change_rate_formatted,
        '上周同一时间的毛利变化率': weekly_change_rate_formatted,
        '前7天的毛利总额': profit_day7_before_yesterday,
        '前7天的平均毛利': average_day7_before_yesterday,
        '昨日同比7日平均变化率': yesterday777_change_rate_formatted
    }

# #调用示例
# result = shujuqingk(open_id='ou_9d42bb88ec8940baf3ad183755131881')
# print(result)

