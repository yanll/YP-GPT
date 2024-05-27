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



def get_this_week_data_in_monitor4_with_params(PAYER_CUSTOMER_SIGNEDNAME:str, ):
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



def get_last_week_data_in_monitor4_with_params():
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


def search_by_customer_no(customer_no: str):
    url = 'https://dmall.yeepay.com/dev-api/dataapi/output/postapi/search_by_CUSTOMER_NO'
    data = {
        "appname": "app",
        "appkey": "yTr5PUeVm6Sw",
        "version": "V1.0",
        "parameters": {
            "CUSTOMER_NO": customer_no
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

def get_total_success_amount_this_week():
    url = 'https://dmall.yeepay.com/dev-api/dataapi/output/postapi/get_this_week_success_amount_in_monitor4'
    data = {
        "appname": "app",
        "appkey": "yTr5PUeVm6Sw",
        "version": "V1.0",
        "parameters": {
        }
    }
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        resp = requests.request('POST', url=url, headers=headers, params={}, data=json.dumps(data))
        resp = resp.json()
        data = resp['data']['data'][0]['SUCCESS_AMOUNT']
    except Exception as e:
        print('监控四获取上周数据异常')
        raise e

    return data


def get_total_success_amount_last_week():
    url = 'https://dmall.yeepay.com/dev-api/dataapi/output/postapi/get_last_week_success_amount_in_monitor4'
    data = {
        "appname": "app",
        "appkey": "yTr5PUeVm6Sw",
        "version": "V1.0",
        "parameters": {
        }
    }
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        resp = requests.request('POST', url=url, headers=headers, params={}, data=json.dumps(data))
        resp = resp.json()
        data = resp['data']['data'][0]['SUCCESS_AMOUNT']
    except Exception as e:
        print('监控四获取上周数据异常')
        raise e

    return data