import requests
import json

def get_refund_rate_in_monitor2(trx_date:str):
    url = 'https://dmall.yeepay.com/dev-api/dataapi/output/postapi/get_refund_rate_in_monitor2'
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
        print('监控四获取本周数据异常')
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
        print('监控四获取上周数据异常')
        raise e

    return data

