import logging

import requests

from dbgpt.extra.dag.buildin_awel.langgraph.wrappers import lark_callback_handler_wrapper
from dbgpt.util import envutils
from dbgpt.util.lark import larkutil, ssoutil


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
            if user_type_value is not None:
                print("成功获取销售看板数据！")
                print("链接userType对应的值为：", user_type_value)
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



