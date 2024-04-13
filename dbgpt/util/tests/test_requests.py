import requests
import json


def test_select_userinfo():
    url = "https://atmgw.yeepay.com/gpt-nc/api/v1/awel/trigger/lark_callback_endpoint"
    # url = "https://c57e-111-198-240-153.ngrok-free.app/api/v1/awel/trigger/lark_callback_endpoint"
    headers = {'Content-Type': 'application/json; charset=utf-8', 'Authorization': '123456'}
    data = {
        "message": "hello!",
        "challenge": "123456"
    }
    resp = requests.request('POST', headers=headers, url=url, data=json.dumps(data))
    print("\n调用返回结果：", resp.text)
    assert True
