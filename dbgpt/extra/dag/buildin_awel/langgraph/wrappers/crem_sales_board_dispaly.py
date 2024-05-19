import logging

import requests

from dbgpt.extra.dag.buildin_awel.langgraph.wrappers import lark_callback_handler_wrapper
from dbgpt.util import envutils
from dbgpt.util.lark import larkutil, ssoutil


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
            nickname = userinfo["name"] + " "
            print("用户的姓名是", nickname)
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
        'yuiassotoken': "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJsb2dpbl90eXBlIjoiQUNDT1VOVCIsIm1vYmlsZSI6IjE4NzU0MzE2MjQwIiwibWlncmF0ZV91c2VyX2lkIjoiZWM4Z2ExYWYiLCJ4LWlwIjoiMTcyLjI1LjI1LjEwIiwicHJpbmNpcGFsX2lkIjoiMTc3OTUiLCJ0b2tlbiI6IjlkMGRhNzc4LWNkNWItNGFmMy05Njg5LTJlNTVlMzIwNzNhMSIsImxvZ2luX25hbWUiOiJodWF4dWUuemhhbmciLCJ0d29fZmFjdG9yX3ZhbGlkIjp0cnVlLCJsb2dpbl90aW1lIjoiMjAyNC0wNS0xOCAxOTo1ODoxNiIsInNjb3BlIjoiIiwiY2FsbGJhY2siOiJodHRwczovL2NlbS55ZWVwYXkuY29tL2luZGV4Lmh0bWwjL2NybS93b3JrUmVwb3J0Iiwic3NvdGlja2V0IjoiYjc3MzE4MWItYTZjOC00MjJhLTk2NTQtYzllMzA0ZDc3ZjE1IiwiZXhwIjoxNzE2MTE5ODk2LCJpYXQiOjE3MTYwMzE2OTYsImVtYWlsIjoiaHVheHVlLnpoYW5nQHllZXBheS5jb20iLCJ1c2VybmFtZSI6IuW8oOWNjumbqiJ9.xbmmYxaXvNDMb6PdxAbjIm9Ykld9wiwzq9brcmW72UhgnR_VDRc8gCIkxAQTUreqyj2mXaIdFcw6PdRyQz2zCA",

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
            print("链接typename的值为：", typename)
            return typename
        else:
            print("请求失败：", response.status_code)
    except Exception as e:
        print("请求时出现异常：", e)




def mobile_process_data(open_id):
    # user_type = 0
    # typename = "金融行业线"
    user_type = sales_board_display(open_id)
    typename = industry_line(open_id)
    if not user_type or not typename:
        return "https://applink.feishu.cn/client/web_url/open?mode=sidebar-semi&reload=false&url=https%3A%2F%2Fopen.feishu.cn%2Fopen-apis%2Fauthen%2Fv1%2Findex%3Fapp_id%3Dcli_a22c1bd8723a500e%26redirect_uri%3Dhttps%253A%252F%252Fhbirdapi.yeepay.com%252Fuia%252Ffeishu%252FexchangeToken%253FexchangeMethod%253Duia%2526appId%253Dcli_a22c1bd8723a500e%2526redirectUrl%253Dhttps%25253A%25252F%25252Fatmgw.yeepay.com%25252Fmcem%25252Findex.html%252523%25252Fcustom%25252Fapp-list%2526apikey%253DajqgGjXTDFQnL1GNKCQqxCiM5tOGmfNd"
    if user_type is not None and typename is not None:
        base_url = "https://img.yeepay.com/hbird-ucm/feishu-web-app-entry/index.html#/app?appId=cli_a22c1bd8723a500e&appEncodeUrl=https://atmgw.yeepay.com/mcem/index.html#/"
        if user_type == 0:
            if typename == "航旅事业部":
                #"销售管理航旅"
                return "https://applink.feishu.cn/client/web_url/open?mode=sidebar-semi&reload=false&url=https%3A%2F%2Fopen.feishu.cn%2Fopen-apis%2Fauthen%2Fv1%2Findex%3Fapp_id%3Dcli_a22c1bd8723a500e%26redirect_uri%3Dhttps%253A%252F%252Fhbirdapi.yeepay.com%252Fuia%252Ffeishu%252FexchangeToken%253FexchangeMethod%253Duia%2526appId%253Dcli_a22c1bd8723a500e%2526redirectUrl%253Dhttps%25253A%25252F%25252Fatmgw.yeepay.com%25252Fmcem%25252Findex.html%252523%25252Fhl%25252FhlsalerMangerView%2526apikey%253DajqgGjXTDFQnL1GNKCQqxCiM5tOGmfNd"
            elif typename == "金融行业线":
                #"销售管理金融"
                return "https://applink.feishu.cn/client/web_url/open?mode=sidebar-semi&reload=false&url=https%3A%2F%2Fopen.feishu.cn%2Fopen-apis%2Fauthen%2Fv1%2Findex%3Fapp_id%3Dcli_a22c1bd8723a500e%26redirect_uri%3Dhttps%253A%252F%252Fhbirdapi.yeepay.com%252Fuia%252Ffeishu%252FexchangeToken%253FexchangeMethod%253Duia%2526appId%253Dcli_a22c1bd8723a500e%2526redirectUrl%253Dhttps%25253A%25252F%25252Fatmgw.yeepay.com%25252Fmcem%25252Findex.html%252523%25252Fjinrong%25252FsaleManageBoard%2526apikey%253DajqgGjXTDFQnL1GNKCQqxCiM5tOGmfNd"
            elif typename == "跨境行业线":
                # "销售管理跨境"
                return "https://applink.feishu.cn/client/web_url/open?mode=sidebar-semi&reload=false&url=https%3A%2F%2Fopen.feishu.cn%2Fopen-apis%2Fauthen%2Fv1%2Findex%3Fapp_id%3Dcli_a22c1bd8723a500e%26redirect_uri%3Dhttps%253A%252F%252Fhbirdapi.yeepay.com%252Fuia%252Ffeishu%252FexchangeToken%253FexchangeMethod%253Duia%2526appId%253Dcli_a22c1bd8723a500e%2526redirectUrl%253Dhttps%25253A%25252F%25252Fatmgw.yeepay.com%25252Fmcem%25252Findex.html%252523%25252Fanalyse%25252Fmanage%2526apikey%253DajqgGjXTDFQnL1GNKCQqxCiM5tOGmfNd"
            else:
                #"销售管理其他"
                return "https://applink.feishu.cn/client/web_url/open?mode=sidebar-semi&reload=false&url=https%3A%2F%2Fopen.feishu.cn%2Fopen-apis%2Fauthen%2Fv1%2Findex%3Fapp_id%3Dcli_a22c1bd8723a500e%26redirect_uri%3Dhttps%253A%252F%252Fhbirdapi.yeepay.com%252Fuia%252Ffeishu%252FexchangeToken%253FexchangeMethod%253Duia%2526appId%253Dcli_a22c1bd8723a500e%2526redirectUrl%253Dhttps%25253A%25252F%25252Fatmgw.yeepay.com%25252Fmcem%25252Findex.html%252523%25252Fanalyse%25252FsaleManageBoard%2526apikey%253DajqgGjXTDFQnL1GNKCQqxCiM5tOGmfNd"

        elif user_type == 1:
            if typename == "航旅事业部":
                #"销售航旅"
                return "https://applink.feishu.cn/client/web_url/open?mode=sidebar-semi&reload=false&url=https%3A%2F%2Fopen.feishu.cn%2Fopen-apis%2Fauthen%2Fv1%2Findex%3Fapp_id%3Dcli_a22c1bd8723a500e%26redirect_uri%3Dhttps%253A%252F%252Fhbirdapi.yeepay.com%252Fuia%252Ffeishu%252FexchangeToken%253FexchangeMethod%253Duia%2526appId%253Dcli_a22c1bd8723a500e%2526redirectUrl%253Dhttps%25253A%25252F%25252Fatmgw.yeepay.com%25252Fmcem%25252Findex.html%252523%25252Fhl%25252FhlsalerView%2526apikey%253DajqgGjXTDFQnL1GNKCQqxCiM5tOGmfNd"
            elif typename == "跨境行业线":
                #"销售跨境"
                return "https://applink.feishu.cn/client/web_url/open?mode=sidebar-semi&reload=false&url=https%3A%2F%2Fopen.feishu.cn%2Fopen-apis%2Fauthen%2Fv1%2Findex%3Fapp_id%3Dcli_a22c1bd8723a500e%26redirect_uri%3Dhttps%253A%252F%252Fhbirdapi.yeepay.com%252Fuia%252Ffeishu%252FexchangeToken%253FexchangeMethod%253Duia%2526appId%253Dcli_a22c1bd8723a500e%2526redirectUrl%253Dhttps%25253A%25252F%25252Fatmgw.yeepay.com%25252Fmcem%25252Findex.html%252523%25252Fsale%25252FchartView%2526apikey%253DajqgGjXTDFQnL1GNKCQqxCiM5tOGmfNd"
            elif typename == "金融行业线":
                return "https://applink.feishu.cn/client/web_url/open?mode=sidebar-semi&reload=false&url=https%3A%2F%2Fopen.feishu.cn%2Fopen-apis%2Fauthen%2Fv1%2Findex%3Fapp_id%3Dcli_a22c1bd8723a500e%26redirect_uri%3Dhttps%253A%252F%252Fhbirdapi.yeepay.com%252Fuia%252Ffeishu%252FexchangeToken%253FexchangeMethod%253Duia%2526appId%253Dcli_a22c1bd8723a500e%2526redirectUrl%253Dhttps%25253A%25252F%25252Fatmgw.yeepay.com%25252Fmcem%25252Findex.html%252523%25252Fjinrong%25252FsaleBoard%2526apikey%253DajqgGjXTDFQnL1GNKCQqxCiM5tOGmfNd"
            else:
                #"销售其他"
                return "https://applink.feishu.cn/client/web_url/open?mode=sidebar-semi&reload=false&url=https%3A%2F%2Fopen.feishu.cn%2Fopen-apis%2Fauthen%2Fv1%2Findex%3Fapp_id%3Dcli_a22c1bd8723a500e%26redirect_uri%3Dhttps%253A%252F%252Fhbirdapi.yeepay.com%252Fuia%252Ffeishu%252FexchangeToken%253FexchangeMethod%253Duia%2526appId%253Dcli_a22c1bd8723a500e%2526redirectUrl%253Dhttps%25253A%25252F%25252Fatmgw.yeepay.com%25252Fmcem%25252Findex.html%252523%25252Fanalyse%25252FsaleBoard%2526apikey%253DajqgGjXTDFQnL1GNKCQqxCiM5tOGmfNd"

        elif user_type == 2:
            #运营权限
            return "https://applink.feishu.cn/client/web_url/open?mode=sidebar-semi&reload=false&url=https%3A%2F%2Fopen.feishu.cn%2Fopen-apis%2Fauthen%2Fv1%2Findex%3Fapp_id%3Dcli_a22c1bd8723a500e%26redirect_uri%3Dhttps%253A%252F%252Fhbirdapi.yeepay.com%252Fuia%252Ffeishu%252FexchangeToken%253FexchangeMethod%253Duia%2526appId%253Dcli_a22c1bd8723a500e%2526redirectUrl%253Dhttps%25253A%25252F%25252Fatmgw.yeepay.com%25252Fmcem%25252Findex.html%252523%25252Fcustom%25252Fapp-list%2526apikey%253DajqgGjXTDFQnL1GNKCQqxCiM5tOGmfNd"
            #return "https://img.yeepay.com/hbird-ucm/feishu-web-app-entry/index.html#/app?appId=cli_a22c1bd8723a500e&appEncodeUrl=https://atmgw.yeepay.com/mcem/index.html#/custom/app-list&exchangeMethod=uia"
        else:
            return "未知用户类型"
    else:
        print("未能获取完整的用户类型和行业线类型，无法进行处理。")
        return "https://applink.feishu.cn/client/web_url/open?mode=sidebar-semi&reload=false&url=https%3A%2F%2Fopen.feishu.cn%2Fopen-apis%2Fauthen%2Fv1%2Findex%3Fapp_id%3Dcli_a22c1bd8723a500e%26redirect_uri%3Dhttps%253A%252F%252Fhbirdapi.yeepay.com%252Fuia%252Ffeishu%252FexchangeToken%253FexchangeMethod%253Duia%2526appId%253Dcli_a22c1bd8723a500e%2526redirectUrl%253Dhttps%25253A%25252F%25252Fatmgw.yeepay.com%25252Fmcem%25252Findex.html%252523%25252Fcustom%25252Fapp-list%2526apikey%253DajqgGjXTDFQnL1GNKCQqxCiM5tOGmfNd"

       # return "未能获取完整的用户类型和行业线类型，无法进行处理。"



