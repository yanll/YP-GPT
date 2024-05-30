import requests
import json

def get_data_by_stat_in_monitor4(trx_date:str, sales_name=None, stat_dispaysignedname=None, payer=None):
    url = 'https://dmall.yeepay.com/dev-api/dataapi/output/postapi/get_data_by_stat_in_montor4'
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
    if payer:
        data['parameters']['PAYER_CUSTOMER_SIGNEDNAME'] = payer
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        resp = requests.request('POST', url=url, headers=headers, params={}, data=json.dumps(data))
        resp = resp.json()
        data = resp['data']['data']
    except Exception as e:
        print('监控四获取数据异常')
        raise e

    return data
