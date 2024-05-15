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




def process_data(open_id):
    user_type = sales_board_display(open_id)
    typename = industry_line(open_id)
    if user_type is not None and typename is not None:
        base_url = "https://img.yeepay.com/hbird-ucm/feishu-web-app-entry/index.html#/app?appId=cli_a22c1bd8723a500e&appEncodeUrl=https://atmgw.yeepay.com/mcem/index.html#/"
        if user_type == 0:
            if typename == "航旅行业线":
                #"销售管理航旅"
                return base_url + "hl/hlsalerMangerView&exchangeMethod=uia"
            elif typename == "金融行业线":
                #"销售管理金融"
                return base_url + "jinrong/saleManageBoard&exchangeMethod=uia"
            else:
                #"销售管理其他"
                return base_url + "analyse/saleManageBoard&exchangeMethod=uia"

        elif user_type == 1:
            if typename == "航旅行业线":
                #"销售航旅"
                return base_url + "hl/hlsalerView&exchangeMethod=uia"
            elif typename == "金融行业线":
                #"销售金融"
                return base_url + "analyse/saleBoard&exchangeMethod=uia"
            else:
                #"销售其他"
                return base_url + "sale/chartView&exchangeMethod=uia"

        elif user_type == 2:
            #运营权限
            return base_url +"custom/app-list&exchangeMethod=uia"
        else:
            return "未知用户类型"
    else:
        return "未能获取完整的用户类型和行业线类型，无法进行处理。"


