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
