import requests
import json

def get_this_week_data_in_monitor4():
    url = 'https://dmall.yeepay.com/dev-api/dataapi/output/postapi/get_this_week_data_in_monitor4'
    data = {
        "appname": "app",
        "appkey": "yTr5PUeVm6Sw",
        "version": "V1.0",
        "parameters": {}
    }
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        resp = requests.request('POST', url=url, headers=headers, params={}, data=json.dumps(data))
        resp = resp.json()
        data = resp['data']['data']
    except Exception as e:
        print('监控四获取本周数据异常')
        raise e

    return data



def get_last_week_data_in_monitor4():
    url = 'https://dmall.yeepay.com/dev-api/dataapi/output/postapi/get_last_week_data_in_monitor4'
    data = {
        "appname": "app",
        "appkey": "yTr5PUeVm6Sw",
        "version": "V1.0",
        "parameters": {}
    }
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        resp = requests.request('POST', url=url, headers=headers, params={}, data=json.dumps(data))
        resp = resp.json()
        data = resp['data']['data']
    except Exception as e:
        print('监控四获取上周数据异常')
        raise e

    return data


def search_by_CUSTOMER_NO(CUSTOMER_NO:str):
    url = 'https://dmall.yeepay.com/dev-api/dataapi/output/postapi/search_by_CUSTOMER_NO'
    data = {
        "appname": "app",
        "appkey": "yTr5PUeVm6Sw",
        "version": "V1.0",
        "parameters": {
            "CUSTOMER_NO": CUSTOMER_NO
        }
    }
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        resp = requests.request('POST', url=url, headers=headers, params={}, data=json.dumps(data))
        resp = resp.json()
        data = resp['data']['data']
    except Exception as e:
        print('监控四获取上周数据异常')
        raise e

    return data