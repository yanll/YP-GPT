import json
import logging

import requests

from dbgpt.util import envutils
from dbgpt.util.lark import ssoutil


def add_daily_or_weekly_report(open_id: str, report_type: str = "", report_time: str = "", work_summary: str = '',
                               senders=None,
                               plans=None):
    url = envutils.getenv("CREM_ENDPOINT") + "/workReportInfo/addWorkReportInfo"
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "yuiassotoken": ssoutil.get_sso_credential(open_id=open_id)
    }

    # bus_plan_list = []
    # if plans:
    #     # 检查第一个元素的类型来决定如何处理整个列表
    #     if isinstance(plans[0], dict):
    #         # 周报的复杂结构处理
    #         for plan in plans:
    #             plan_dict = {
    #                 "planContentString": plan.get("planContentString", ""),
    #                 "customerNo": plan.get("customerNo", ""),
    #                 "customerName": plan.get("customerName", "")
    #             }
    #             bus_plan_list.append(plan_dict)
    #     else:
    #         # 日报的简单字符串列表处理
    #         for plan in plans:
    #             plan_dict = {"planContentString": plan}
    #             bus_plan_list.append(plan_dict)

    data = {
        "reportTitle": "",
        "reportType": report_type,
        "reportTime": report_time,
        "workSummaryString": work_summary,
        "busPlanForTomorrowInfoList": [],
        "busWorkScheduleInfoList": [],
        "busAnnexInfos": []
    }
    # ,
    # "senders": senders if senders else "",
    # "busPlanForTomorrowInfoList": [plans],
    # "busPlanForTomorrowInfoList": [],
    # "busWorkScheduleInfoList": [],
    # "busAnnexInfos": []
    print("提交日报到CREM：", data)
    response = requests.post(url, headers=headers, data=json.dumps(data))
    try:
        print(response.json())
    except Exception as e:
        print(response)
        logging.error("CREM日报调用失败：", e)
        raise e
    return response


def add_crm_bus_customer(open_id: str,
                         customer_name: str = "",
                         customer_role: str = "",
                         customer_source: str = '',
                         customer_importance: str = '',
                         sale_name: str = '',
                         industry_line: str = '',
                         business_type: str = '',
                         product_type: str = '',
                         zw_client_assets: str = '',
                         zw_business_type: str = '',
                         zw_province: str = '',
                         zw_system_vendor: str = '',
                         zw_signed_annual_gross_profit: str = '',
                         zw_customer_level: str = '',
                         customer_size: str = '',
                         customer_profile: str = '',
                         important_step: str = '',
                         purchasing_channels: str = '',
                         payment_scene: str = '',
                         sales_channel: str = '',
                         ):
    url = envutils.getenv("CREM_ENDPOINT") + "/crmCustomer/addCrmBusCustomer"
    headers = {
        "pagetype": "cemPortal",
        "Content-Type": "application/json; charset=utf-8",
        "yuiassotoken": ssoutil.get_sso_credential(open_id=open_id)
    }

    data = {
        "busCrmCustomerMerchantRelationList": [
            {
                "association": "同一资质",
                "enterpriseName": customer_name
            }
        ],
        "busCrmCustomerProductList": [
            {
                "productType": product_type,
                "productEntrance": "",
                "id": ""
            }
        ],
        "businessType": business_type,
        "customerName": customer_name,
        "customerRole": customer_role,
        "customerSource": customer_source,
        "industryLine": industry_line,
        "saleName": sale_name,
        "customerImportance": customer_importance,

        "zwClientAssets": zw_client_assets,
        "zwBusinessType": zw_business_type,
        "zwProvince": zw_province,
        "zwSystemVendor": zw_system_vendor,
        "zwSignedAnnualGrossProfit": zw_signed_annual_gross_profit,
        "zwCustomerLevel": zw_customer_level,
        "customerSize": customer_size,
        "customerProfile": customer_profile,
        "importantStep": important_step

    }
    print("提交添加报单客户信息到CREM：", data)
    response = requests.post(url, headers=headers, data=json.dumps(data))
    try:
        print(response.json())
    except Exception as e:
        print(response)
        logging.error("CREM添加报单客户信息调用失败：", e)
        raise e
    return response


def get_crm_user_industry_line(open_id: str) -> str:
    url = envutils.getenv("CREM_ENDPOINT") + "/common/treeDictionary"
    headers = {
        "pagetype": "cemPortal",
        "Content-Type": "application/json; charset=utf-8",
        "yuiassotoken": ssoutil.get_sso_credential(open_id=open_id)
    }

    data = {
        "type": "49"
    }
    print("开始获取用户行业线")
    response = requests.post(url, headers=headers, data=json.dumps(data))
    try:
        print(response.json())
        resp = response.json()
        if response.status_code != 200:
            logging.error("用户凭证接口异常：" + str(response.status_code))
            raise ValueError("获取用户行业线失败" + str(response.status_code))
        print(resp['data'])
        if len(resp['data']) == 0:
            return ''
        return resp['data'][0]['typename']

    except Exception as e:
        logging.error("crm获取用户行业线", e)
        raise e
    return ''


def get_crm_user_name(open_id: str) -> str:
    url = envutils.getenv("CREM_ENDPOINT") + "/user/userInfoByUserId"
    headers = {
        "pagetype": "cemPortal",
        "Content-Type": "application/json; charset=utf-8",
        "yuiassotoken": ssoutil.get_sso_credential(open_id=open_id)
    }

    data = {
    }
    print("开始获取用户信息")
    response = requests.post(url, headers=headers, data=json.dumps(data))
    try:
        print(response.json())
        resp = response.json()
        if response.status_code != 200:
            logging.error("用户凭证接口异常：" + str(response.status_code))
            raise ValueError("获取用户信息失败" + str(response.status_code))
        print(resp['data'])
        if len(resp['data']) == 0:
            return ''
        return resp['data']['username']

    except Exception as e:
        logging.error("crm获取用户行业线", e)
        raise e
    return ''

# Example usage for daily and weekly reports
# 日报

# # 周报
# weekly_report_type = "周报"
# weekly_report_time = "2024-04-28 00:00:00"
# weekly_work_summary = "本周完成了项目A的设计，解决了项目B中的一些问题"
# weekly_senders = "张华雪"
# weekly_plans = [
#     {"planContentString": "下周继续完成项目A", "customerNo": "KA2024-A04220001", "customerName": "客户X"},
# ]
# weekly_result = add_report(weekly_report_type, weekly_report_time, weekly_work_summary, weekly_senders, weekly_plans)
# print("周报结果:", weekly_result)
