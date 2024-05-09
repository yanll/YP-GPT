import json

import requests

from dbgpt.util.lark.larkutil import build_headers


def muti_table_create(name: str, folder_token: str):
    """
    创建多维表格
    """
    url = 'https://open.feishu.cn/open-apis/bitable/v1/apps'
    data = {
        "name": name,
        "folder_token": folder_token
    }
    resp = requests.request('POST', url=url, headers=build_headers(), params={}, data=json.dumps(data))
    print('多维表格创建返回结果：', resp.json())
    if resp.json().get('code') == 0:
        print('多维表格创建完成：', resp.json()['data'])
    else:
        print('多维表格创建失败：', resp.json())
    return resp.json()


def muti_table_add_record(app_id, table_id, record):
    """
    多维表格插入记录
    """
    url = ('https://open.feishu.cn/open-apis/bitable/v1/apps/{app_id}/tables/{table_id}/records'
           .format(app_id=app_id, table_id=table_id))
    params = {
        "ts": "123456"
    }
    data = json.dumps(record)
    resp = requests.request('POST', url=url, headers=build_headers(), params=params, data=data)
    print('多维表格添加记录返回结果：', resp.json())
    if resp.json().get('code') == 0:
        print('添加记录完成：', resp.json()['data'])
    else:
        print('添加记录失败：', resp.json())
    return resp.json()
