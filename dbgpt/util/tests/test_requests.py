import requests
import json


def test_select_userinfo():
    url = "https://atmgw.yeepay.com/gpt-nc/api/v1/awel/trigger/lark_callback_endpoint"
    headers = {'Content-Type': 'application/json; charset=utf-8', 'Authorization': '123456'}
    data = {
        "context": {
            "conv_uid": "123456"
        },
        "message": "查询商户编号是10012982662的商户详细信息"
    }
    resp = requests.request('POST', headers=headers, url=url, data=json.dumps(data))
    print("调用返回结果：", resp.text)
    assert True
