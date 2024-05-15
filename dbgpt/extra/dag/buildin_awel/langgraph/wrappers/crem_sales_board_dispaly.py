import logging

import requests

from dbgpt.extra.dag.buildin_awel.langgraph.wrappers import lark_callback_handler_wrapper
from dbgpt.util.lark import larkutil, ssoutil


def sales_board_display(open_id=None):
    global nickname
    url = 'https://nccemportal.yeepay.com/cem-api/crmCustomer/getSuperiorAndSubordinate'
    headers = {
        'yuiassotoken': ssoutil.get_sso_credential(open_id),
        'pageType': 'cemPortal',
        #'Content-Type': 'application/json',

    }

    # try:
    #     ss = larkutil.select_userinfo(open_id)
    #     if ss and "name" in ss:
    #         nickname = ss["name"] + " "
    # except Exception as e:
    #     logging.warning("用户姓名解析异常：", open_id)
    # # userinfo = larkutil.select_userinfo(open_id)
    # # if userinfo and "name" in userinfo:
    # #     nickname = userinfo["name"] + " "
    # # print("用户的姓名是",nickname)

    data = {
        "requestParams": "SUPERIOR_NAME",
        "targetParams": "SALES_NAME",
        "userName": "张华雪"
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            # user_type_value = result.get('data',{}).get('userType',"")
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
# # 调用函数以获取销售看板数据
# sales_board_display()


def industry_line(open_id=None):
    url = 'https://nccemportal.yeepay.com/cem-api/common/treeDictionary'
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
            print("typename的值为：",typename)
            return typename
        else:
            print("请求失败：", response.status_code)
    except Exception as e:
        print("请求时出现异常：", e)


# # 调用函数以获取行业线数据
# industry_line()

def process_data(open_id):
    user_type = sales_board_display(open_id)
    typename = industry_line(open_id)
    if user_type is not None and typename is not None:
        if user_type == 0:
            if typename == "大零售行业线":
                return "销售管理大零售"
            elif typename == "金融行业线":
                return "销售管理金融"
            else:
                return "销售管理其他"
        elif user_type == 1:
            if typename == "大零售行业线":
                return "https://img.yeepay.com/hbird-ucm/feishu-web-app-entry/index.html#/app?appId=cli_a22c1bd8723a500e&appEncodeUrl=https://atmgw.yeepay.com/mcem/index.html#/analyse/manage&exchangeMethod=uia"
                #return "https://img.yeepay.com/hbird-ucm/feishu-web-app-entry/index.html#/app?appId=cli_a22c1bd8723a500e&appEncodeUrl=https://cem.yeepay.com/index.html#/workspace/workspace&exchangeMethod=uia"
            elif typename == "金融行业线":
                return "销售金融"
            else:
                return "销售其他"
        elif user_type == 2:
            return "https://img.yeepay.com/hbird-ucm/feishu-web-app-entry/index.html#/app?appId=cli_a22c1bd8723a500e&appEncodeUrl=https://atmgw.yeepay.com/mcem/index.html#/analyse/manage&exchangeMethod=uia"
        else:
            return "未知用户类型"
    else:
        return "未能获取完整的用户类型和行业线类型，无法进行处理。"


# # 获取用户类型和行业线类型
# user_type = sales_board_display()
# typename = industry_line()
# # 如果用户类型和行业线类型都不为None，则进行处理
# result = process_data(user_type, typename)
# print("处理后的结果为：", result)
