import requests
import json
import jwt


def test_lark_event_endpoint():
    url = "http://127.0.0.1:5670/api/v1/awel/trigger/lark_event_endpoint"
    headers = {'Content-Type': 'application/json; charset=utf-8', 'Authorization': '123456'}
    data = {'schema': '2.0',
            'header': {'event_id': 'a556f6edb6433b49a0ed5e28354d18f2', 'token': 'eXtQhf4KFW3UCoG7SRSVtdranM5BrsNW',
                       'create_time': '1713174740198', 'event_type': 'im.message.receive_v1',
                       'tenant_key': '2cfa3e0dad8cd75d', 'app_id': 'cli_9f6b79a9e737900b'}, 'event': {
            'message': {'chat_id': 'oc_db3dcc0ff9c6d494a07527e363a5861c', 'chat_type': 'p2p',
                        'content': '{"text":"和客户交流了合作方案"}', 'create_time': '1713174739807',
                        'message_id': 'om_5b624dce3d5a4ad203e55126668a5ab7', 'message_type': 'text',
                        'update_time': '1713174739807'}, 'sender': {
                'sender_id': {'open_id': 'ou_1a32c82be0a5c6ee7bc8debd75c65e34',
                              'union_id': 'on_0ee3e44cbecb75e4e680bc62eabbebf5',
                              'user_id': 'ecd502d4-2e68-44b5-a25f-f21fd33b1520'}, 'sender_type': 'user',
                'tenant_key': '2cfa3e0dad8cd75d'}}}
    resp = requests.request('POST', headers=headers, url=url, data=json.dumps(data))
    print("\n调用返回结果：", resp.text)
    assert True


def test_calendar_endpoint():
    url = "http://127.0.0.1:5670/api/v1/awel/trigger/calendar_endpoint"
    headers = {'Content-Type': 'application/json; charset=utf-8', 'Authorization': '123456'}
    data = {'schema': '2.0',
            'header': {'event_id': 'a556f6edb6433b49a0ed5e28354d18f2', 'token': 'eXtQhf4KFW3UCoG7SRSVtdranM5BrsNW',
                       'create_time': '1713174740198', 'event_type': 'im.message.receive_v1',
                       'tenant_key': '2cfa3e0dad8cd75d', 'app_id': 'cli_9f6b79a9e737900b'}, 'event': {
            'message': {'chat_id': 'oc_db3dcc0ff9c6d494a07527e363a5861c', 'chat_type': 'p2p',
                        'content': '{"text_":"你好","text":"我需要预定明天下午3点到4点的极致会议室！"}',
                        'create_time': '1713174739807',
                        'message_id': 'om_5b624dce3d5a4ad203e55126668a5ab7', 'message_type': 'text',
                        'update_time': '1713174739807'}, 'sender': {
                'sender_id': {'open_id': 'ou_1a32c82be0a5c6ee7bc8debd75c65e34',
                              'union_id': 'on_0ee3e44cbecb75e4e680bc62eabbebf5',
                              'user_id': 'ecd502d4-2e68-44b5-a25f-f21fd33b1520'}, 'sender_type': 'user',
                'tenant_key': '2cfa3e0dad8cd75d'}}}
    resp = requests.request('POST', headers=headers, url=url, data=json.dumps(data))
    print("\n调用返回结果：", resp.text)
    assert True


ttt = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJsb2dpbl90eXBlIjoiQUNDT1VOVCIsIm1vYmlsZSI6IjE4NjExNzAwMzgwIiwibWlncmF0ZV91c2VyX2lkIjoibGlhbmdsaWFuZy55YW5AeWVlcGF5LmNvbSIsIngtaXAiOiIxMjcuMC4wLjEiLCJwcmluY2lwYWxfaWQiOiIxMDAiLCJ0b2tlbiI6IjkxNGQ0MDE3LTY0M2ItNDUxZC1hN2I4LTg4NGMxNzRlNzBkNCIsImxvZ2luX25hbWUiOiJsaWFuZ2xpYW5nLnlhbiIsInR3b19mYWN0b3JfdmFsaWQiOnRydWUsImxvZ2luX3RpbWUiOiIyMDI0LTA1LTA4IDIyOjA4OjAyIiwic2NvcGUiOiIiLCJjYWxsYmFjayI6IiIsInNzb3RpY2tldCI6ImZtYy1ib3NzIiwiZXhwIjoxNzE1MjQ5MjgyLCJpYXQiOjE3MTUxMDUyODIsImVtYWlsIjoibGlhbmdsaWFuZy55YW5AeWVlcGF5LmNvbSIsInVzZXJuYW1lIjoi5Lil5Lqu5LquIn0.pdegHwm_832EjPuTh5_vv3ClF5TyFOl0F6-4mfrmYL-YTAMARPRzAc4qpD8L8mZ9zuHP0gXQPhsGD7-0uoXd2g";


def test_sso():
    url = "http://127.0.0.1:30992/proc-console/auth/agent"
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    data = {
        "en_name": "liangliang.yan",
        "name": "严亮亮",
        "email": "liangliang.yan@yeepay.com",
        "mobile": "18611700380"
    }
    resp = requests.request('POST', headers=headers, url=url, data=json.dumps(data))
    print("\n调用返回结果：", resp.text)

    dict = resp.json()
    token = dict["data"]
    print("TOKEN:\n")
    print(token)
    assert True


def test_crem():
    # url = "https://nccemportal.yeepay.com/cem-api/comprehensiveSearch/_search"
    url = "http://ycetest.yeepay.com:30762/cem-api/comprehensiveSearch/_search"
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json; charset=utf-8',
        'yuiassotoken': ttt
    }
    data = {
        "customerRole": "",
        "customerServiceLevel": "",
        "exclusiveOperation": "",
        "level1Info": "",
        "level2Info": "",
        "lifeCycle": "",
        "industryLine": "",
        "satisfaction": "",
        "pageSize": 20,
        "pageNum": 1,
        "isfollow": "",
        "importantCustomer": "",
        "clusterNo": "",
        "clusterName": ""
    }
    resp = requests.request('POST', headers=headers, url=url, data=json.dumps(data))
    print("\n调用返回结果：", resp.text)
    assert True


def test_fmc():
    # url = "https://nccemportal.yeepay.com/cem-api/comprehensiveSearch/_search"
    url = "http://ycetest.yeepay.com:30666/fmc-boss/flowable/task/list"
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json; charset=utf-8',
        'Authorization': ttt
    }
    params = {
        "ssssss": "1234567890111111",
        "page": 1,
        "limit": 10,
    }
    cookies = {'ssoticket': 'fmc-boss'}

    resp = requests.request('GET', cookies=cookies, headers=headers, url=url, params=params)
    print("\n调用返回结果：", resp.text)
    assert True


def test_iam():
    # url = "https://nccemportal.yeepay.com/cem-api/comprehensiveSearch/_search"
    url = "http://ycetest.yeepay.com:30987/console/app/list?p=123456"
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'Authorization': ttt
    }
    params = {
        "ssssss": "1234567890111111",
        "page": 1,
        "limit": 10,
    }
    resp = requests.request('GET', headers=headers, url=url, params=params)
    print("\n调用返回结果：", resp.text)
    assert True


def test_appcenter():
    # url = "https://nccemportal.yeepay.com/cem-api/comprehensiveSearch/_search"
    url = "http://ycetest.yeepay.com:49357/appcenter/application/?pageNum=1&pageSize=10&appName="
    headers = {
        'Accept': 'application/json, text/plain, */*',

        'Content-Type': 'application/json; charset=utf-8',
        'yuiassotoken': ttt
    }
    params = {
        "ssssss": "1234567890111111",
        "page": 1,
        "limit": 10,
    }
    cookies = {'ssoticket': 'fmc-boss'}

    resp = requests.request('GET', cookies=cookies, headers=headers, url=url, params=params)
    print("\n调用返回结果：", resp.text)
    assert True

# 014ac59b-44a9-479e-bf44-8346eae7e5df
