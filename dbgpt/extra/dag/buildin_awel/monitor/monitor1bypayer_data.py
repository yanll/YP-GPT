import requests
import json

def get_data_by_payer_in_monitor1(trx_date:str, payer_sales_name=None, payer_customer_signedname=None):
    url = 'https://dmall.yeepay.com/dev-api/dataapi/output/postapi/get_data_by_payer_in_montor1'
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
        print('监控一获取数据异常')
        raise e

    return data

def get_industry_line_data_by_payer_in_monitor1(trx_date:str):
    url = 'https://dmall.yeepay.com/dev-api/dataapi/output/postapi/get_industry_line_data_by_payer_in_montor1'
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


def get_reason_4_data_by_payer_in_monitor1(trx_date:str, payer_sales_name:str, payer_customer_signedname:str):
    url = 'https://dmall.yeepay.com/dev-api/dataapi/output/postapi/get_reason_4_data_by_payer_in_montor1'
    data = {
        "appname": "app",
        "appkey": "yTr5PUeVm6Sw",
        "version": "V1.0",
        "parameters": {
            'TRX_DATE': trx_date,
            'PAYER_SALES_NAME': payer_sales_name,
            'PAYER_CUSTOMER_SIGNEDNAME': payer_customer_signedname
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
        print('监控一归因四获取数据异常')
        raise e

    return data



def get_reason_5_data_by_payer_in_monitor1(trx_date:str, payer_sales_name:str, payer_customer_signedname:str):
    url = 'https://dmall.yeepay.com/dev-api/dataapi/output/postapi/get_reason_5_data_by_payer_in_montor1'
    data = {
        "appname": "app",
        "appkey": "yTr5PUeVm6Sw",
        "version": "V1.0",
        "parameters": {
            'TRX_DATE': trx_date,
            'PAYER_SALES_NAME': payer_sales_name,
            'PAYER_CUSTOMER_SIGNEDNAME': payer_customer_signedname
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
        print('监控一归因四获取数据异常')
        raise e

    return data