import requests
import json

def get_data_by_stat_in_monitor2(trx_date:str, sales_name=None, stat_dispaysignedname=None):
    url = 'https://dmall.yeepay.com/dev-api/dataapi/output/postapi/get_data_by_stat_in_montor2'
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
        print('监控二获取数据异常')
        raise e

    return data

def get_data_by_payer_in_monitor2(trx_date:str, payer_sales_name=None, payer_customer_signedname=None):
    url = 'https://dmall.yeepay.com/dev-api/dataapi/output/postapi/get_data_by_payer_in_montor2'
    data = {
        "appname": "app",
        "appkey": "yTr5PUeVm6Sw",
        "version": "V1.0",
        "parameters": {
            'TRX_DATE': trx_date
        }
    }
    if payer_sales_name:
        data['parameters']['PAYER_SALES_NAME'] = payer_sales_name
    if payer_customer_signedname:
        data['parameters']['PAYER_CUSTOMER_SIGNEDNAME'] = payer_customer_signedname
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