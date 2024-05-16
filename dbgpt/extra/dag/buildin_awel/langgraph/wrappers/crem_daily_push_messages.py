import logging

import requests
import json
from datetime import datetime, timedelta

from dbgpt.util import envutils
from dbgpt.util.lark import larkutil, ssoutil

global nickname

def sales_board_display(open_id):
    global nickname
    url = envutils.getenv("CREM_ENDPOINT") + '/crmCustomer/getSuperiorAndSubordinate'

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

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            user_type_value = result.get('data', {}).get('userType')
            if user_type_value:
                print("成功获取销售看板数据！")
                print("userType对应的值为：", user_type_value)
                return user_type_value
            else:
                print("未找到userType对应的值")
        else:
            print("获取销售看板数据失败：", response.status_code)
    except Exception as e:
        print("获取销售看板数据时出现异常：", e)





def industry_line(open_id=None):
    url = envutils.getenv("CREM_ENDPOINT") + '/common/treeDictionary'

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
            print("typename的值为：", typename)
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
    try:
        userinfo = larkutil.select_userinfo(open_id=open_id)
        if userinfo and "name" in userinfo:
            nickname = userinfo["name"] + " "
            print("用户的姓名是", nickname)
    except Exception as e:
        logging.warning("用户姓名解析异常：", open_id)

    # typename = industry_line(open_id)
    # # 根据行业线的值选择不同的url和data
    # if typename == "航旅行业线":
    url = envutils.getenv(
        "CREM_ENDPOINT_APP") + '/mobile/aggScript/wrap/apis/receive/handleApplicationMarketplace/hv_jf_day_summary_situate_one'
    headers = {
        'yuiassotoken': ssoutil.get_sso_credential(open_id),
        'pageType': 'cemPortal',
        'Content-Type': 'application/json',
    }
    data = {
        "parameters": {
            "TYPE": "航司,渠道,酒旅出行",
            "SCALE_TYPE": "DAY",
            "TRX_DATE": trx_date,
            "STAT_SALES_NAME": nickname
        },
        "strategyKey": "saleOrdinaryApplicationMarketExecutor"
    }

    # elif typename == "跨境行业线":
    #     url = envutils.getenv(
    #         "CREM_ENDPOINT_APP") + '/mobile/threeParty/wrap/apis/agg/crem_salesmanage_kj_ydd_hzqk'
    #     headers = {
    #         'yuiassotoken': ssoutil.get_sso_credential(open_id),
    #         'pageType': 'cemPortal',
    #         'Content-Type': 'application/json',
    #     }
    #     data = {
    #         "tenant": "default",
    #         "procDefKey": "dmallGeneral",
    #         "data": {
    #             "dmallReq": {
    #                 "parameters": {
    #                     "TRX_DATE": trx_date,
    #                     "MERCHANT_SALESNAME": "柳永亮"
    #                 },
    #                 "url": "crem_salesmanage_kj_ydd_hzqk",
    #                 "version": "V1.0"
    #             }
    #         }
    #     }
    # else:
    #     url = envutils.getenv(
    #         "CREM_ENDPOINT_APP") + '/mobile/aggScript/wrap/apis/receive/handleApplicationMarketplace/hv_jf_day_summary_situate_one'
    #     headers = {
    #         'yuiassotoken': ssoutil.get_sso_credential(open_id),
    #         'pageType': 'cemPortal',
    #         'Content-Type': 'application/json',
    #     }
    #     data = {
    #         "parameters": {
    #             "TYPE": "航司,渠道,酒旅出行",
    #             "SCALE_TYPE": "DAY",
    #             "TRX_DATE": trx_date,
    #             "STAT_SALES_NAME": nickname
    #         },
    #         "strategyKey": "saleOrdinaryApplicationMarketExecutor"
    #     }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    # 检查响应状态码
    if response.status_code == 200:
        try:
            # 尝试解析JSON数据
            json_data = response.json()
            # 判断返回值中是否有指定字段且不为null
            if "data" in json_data and json_data["data"] and "TRX_PROFIT" in json_data["data"] and json_data["data"][
                "TRX_PROFIT"] is not None:
                return json_data
            else:
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
    yesterday, day_before_yesterday, day7_before_yesterday, weekly_before_today = get_previous_dates()
    trx_date_yesterday = f"{yesterday},{yesterday}"
    trx_date_day_before_yesterday = f"{day_before_yesterday},{day_before_yesterday}"
    trx_date_day7_before_yesterday = f"{day7_before_yesterday},{yesterday}"
    trx_date_weekly_before_today = f"{weekly_before_today},{weekly_before_today}"

    # 调用函数并获取结果
    result_yesterday = maolicase(trx_date_yesterday,open_id)
    result_day_before_yesterday = maolicase(trx_date_day_before_yesterday,open_id)
    result_day7_before_yesterday = maolicase(trx_date_day7_before_yesterday,open_id)
    result_weekly_before_today = maolicase(trx_date_weekly_before_today,open_id)

    # 检查是否进行了非正常查询
    if 'error' in result_yesterday or 'error' in result_day_before_yesterday or 'error' in result_day7_before_yesterday or 'error' in result_weekly_before_today:
        # 如果进行了非正常查询，则返回所有毛利字段的值为"数据为空"
        profit_yesterday = "数据为空"
        profit_day_before_yesterday = "数据为空"
        profit_day7_before_yesterday = "数据为空"
        average_day7_before_yesterday = "数据为空"
        yesterday_change_rate = "数据为空"
        weekly_change_rate_formatted = "数据为空"
    else:
        # 提取毛利数据并格式化
        profit_yesterday = format_profit(result_yesterday['data']['TRX_PROFIT'])
        profit_day_before_yesterday = format_profit(result_day_before_yesterday['data']['TRX_PROFIT'])
        profit_day7_before_yesterday = format_profit(result_day7_before_yesterday['data']['TRX_PROFIT'])

        # 计算前7天平均每日毛利
        if result_day7_before_yesterday['data']['TRX_PROFIT'] is None:
            average_day7_before_yesterday = "数据为空"
        else:
            average_day7_before_yesterday = format_profit(result_day7_before_yesterday['data']['TRX_PROFIT'] / 7)

        # 计算昨天相对于前天的同比变化率
        profit_yesterday_x = float(result_yesterday['data']['TRX_PROFIT'])
        profit_day_before_yesterday_x = float(result_day_before_yesterday['data']['TRX_PROFIT'])
        yesterday_change_rate = ((profit_yesterday_x - profit_day_before_yesterday_x) / profit_day_before_yesterday_x) * 100

        # 计算上周同一时间的毛利变化率
        profit_weekly_before_today_x = float(result_weekly_before_today['data']['TRX_PROFIT'])
        weekly_change_rate = ((profit_yesterday_x - profit_weekly_before_today_x) / profit_weekly_before_today_x) * 100
        weekly_change_rate_formatted = "{:.2f}%".format(weekly_change_rate)

    # 返回数据字典
    return {
        '昨天的毛利': profit_yesterday,
        '前天的毛利': profit_day_before_yesterday,
        '昨天相对于前天的同比变化率': yesterday_change_rate,
        '上周同一时间的毛利变化率': weekly_change_rate_formatted,
        '前7天的毛利总额': profit_day7_before_yesterday,
        '前7天的平均毛利': average_day7_before_yesterday
    }


# def shujuqingk(open_id):
#
#     # 获取昨天和前天的日期
#     yesterday, day_before_yesterday, day7_before_yesterday, weekly_before_today = get_previous_dates()
#
#     # 构造时间参数
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
#     # 提取毛利数据并格式化
#     profit_yesterday = "数据为空" if result_yesterday['data']['TRX_PROFIT'] is None else format_profit(result_yesterday['data']['TRX_PROFIT'])
#     profit_day_before_yesterday = "数据为空" if result_day_before_yesterday['data']['TRX_PROFIT'] is None else format_profit(result_day_before_yesterday['data']['TRX_PROFIT'])
#     profit_day7_before_yesterday = "数据为空" if result_day7_before_yesterday['data']['TRX_PROFIT'] is None else format_profit(result_day7_before_yesterday['data']['TRX_PROFIT'])
#     profit_weekly_before_today = "数据为空" if result_weekly_before_today['data']['TRX_PROFIT'] is None else format_profit(result_weekly_before_today['data']['TRX_PROFIT'])
#
#     # 计算前7天平均每日毛利
#     if result_day7_before_yesterday['data']['TRX_PROFIT'] is None:
#         average_day7_before_yesterday = "数据为空"
#     else:
#         average_day7_before_yesterday = format_profit(result_day7_before_yesterday['data']['TRX_PROFIT'] / 7)
#
#     # 计算同比变化率
#     if result_yesterday['data']['TRX_PROFIT'] is not None and result_day_before_yesterday['data']['TRX_PROFIT'] is not None:
#         profit_yesterday_x = float(result_yesterday['data']['TRX_PROFIT'])
#         profit_day_before_yesterday_x = float(result_day_before_yesterday['data']['TRX_PROFIT'])
#         yesterday_change_rate = ((profit_yesterday_x - profit_day_before_yesterday_x) / profit_day_before_yesterday_x) * 100
#     else:
#         yesterday_change_rate = "数据为空"
#
#     if result_yesterday['data']['TRX_PROFIT'] is not None and result_weekly_before_today['data']['TRX_PROFIT'] is not None:
#         profit_yesterday_x = float(result_yesterday['data']['TRX_PROFIT'])
#         profit_weekly_before_today_x = float(result_weekly_before_today['data']['TRX_PROFIT'])
#         weekly_change_rate = ((profit_yesterday_x - profit_weekly_before_today_x) / profit_weekly_before_today_x) * 100
#         weekly_change_rate_formatted = "{:.2f}%".format(weekly_change_rate)
#     else:
#         weekly_change_rate_formatted = "数据为空"
#
#     # 返回数据字典
#     return {
#         '昨天的毛利': profit_yesterday,
#         '前天的毛利': profit_day_before_yesterday,
#         '昨天相对于前天的同比变化率': yesterday_change_rate,
#         '上周同一时间的毛利变化率': weekly_change_rate_formatted,
#         '前7天的毛利总额': profit_day7_before_yesterday,
#         '前7天的平均毛利': average_day7_before_yesterday
#     }

