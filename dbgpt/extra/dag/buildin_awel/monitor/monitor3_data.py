import requests
import json

def get_success_amount_by_stat_in_monitor3(trx_date:str):
    url = 'https://dmall.yeepay.com/dev-api/dataapi/output/postapi/get_success_amount_by_stat_in_monitor3'
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
        print('监控二获取数据异常')
        raise e

    return data


def get_success_amount_by_payer_in_monitor3(trx_date:str):
    url = 'https://dmall.yeepay.com/dev-api/dataapi/output/postapi/get_success_amount_by_payer_in_monitor3'
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
        print('监控二获取数据异常')
        raise e

    return data

def search_by_stat_dispaysignedname(stat_dispaysignedname: str):
    url = 'https://dmall.yeepay.com/dev-api/dataapi/output/postapi/search_by_stat_dispaysignedname'
    data = {
        "appname": "app",
        "appkey": "yTr5PUeVm6Sw",
        "version": "V1.0",
        "parameters": {
            "STAT_DISPAYSIGNEDNAME": stat_dispaysignedname
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
        print('监控二获取销售数据异常')
        raise e

    return data
