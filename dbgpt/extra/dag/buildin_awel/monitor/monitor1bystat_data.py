import requests
import json

def get_data_by_stat_in_monitor1(trx_date:str, sales_name=None, stat_dispaysignedname=None):
    url = 'https://dmall.yeepay.com/dev-api/dataapi/output/postapi/get_data_by_stat_in_montor1'
    data = {
        "appname": "app",
        "appkey": "yTr5PUeVm6Sw",
        "version": "V1.0",
        "parameters": {
            'TRX_DATE': trx_date
        }
    }
    if sales_name:
        data['parameters']['SALES_NAME'] = sales_name
    if stat_dispaysignedname:
        data['parameters']['STAT_DISPAYSIGNEDNAME'] = stat_dispaysignedname
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        resp = requests.request('POST', url=url, headers=headers, params={}, data=json.dumps(data))
        resp = resp.json()
        data = resp['data']['data']
    except Exception as e:
        print('监控一获取数据异常')
        raise e

    return data


def get_industry_line_data_by_stat_in_monitor1(trx_date:str):
    url = 'https://dmall.yeepay.com/dev-api/dataapi/output/postapi/get_industry_line_data_by_stat_in_montor1'
    data = {
        "appname": "app",
        "appkey": "yTr5PUeVm6Sw",
        "version": "V1.0",
        "parameters": {
            'TRX_DATE': trx_date
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
        print('监控一获取数据异常')
        raise e

    return data

def get_reason_1_data_by_stat_in_monitor1(trx_date:str, sales_name:str, stat_dispaysignedname:str):
    url = 'https://dmall.yeepay.com/dev-api/dataapi/output/postapi/get_reason_1_data_by_stat_in_montor1'
    data = {
        "appname": "app",
        "appkey": "yTr5PUeVm6Sw",
        "version": "V1.0",
        "parameters": {
            'TRX_DATE': trx_date,
            'SALES_NAME': sales_name,
            'STAT_DISPAYSIGNEDNAME': stat_dispaysignedname
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
        print('监控一归因一获取数据异常')
        raise e

    return data


def get_reason_2_data_by_stat_in_monitor1(trx_date:str, sales_name:str, stat_dispaysignedname:str):
    url = 'https://dmall.yeepay.com/dev-api/dataapi/output/postapi/get_reason_2_data_by_stat_in_montor1'
    data = {
        "appname": "app",
        "appkey": "yTr5PUeVm6Sw",
        "version": "V1.0",
        "parameters": {
            'TRX_DATE': trx_date,
            'SALES_NAME': sales_name,
            'STAT_DISPAYSIGNEDNAME': stat_dispaysignedname
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
        print('监控一归因二获取数据异常')
        raise e

    return data

def get_reason_3_data_by_stat_in_monitor1(trx_date:str, sales_name:str, stat_dispaysignedname:str):
    url = 'https://dmall.yeepay.com/dev-api/dataapi/output/postapi/get_reason_3_data_by_stat_in_montor1'
    data = {
        "appname": "app",
        "appkey": "yTr5PUeVm6Sw",
        "version": "V1.0",
        "parameters": {
            'TRX_DATE': trx_date,
            'SALES_NAME': sales_name,
            'STAT_DISPAYSIGNEDNAME': stat_dispaysignedname
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
        print('监控一归因三获取数据异常')
        raise e

    return data