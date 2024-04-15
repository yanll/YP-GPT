import requests
import json


def test_select_userinfo():
    url = "http://127.0.0.1:3000/api/v1/awel/trigger/lark_event_endpoint"
    headers = {'Content-Type': 'application/json; charset=utf-8', 'Authorization': '123456'}
    data = {'schema': '2.0',
            'header': {'event_id': 'a556f6edb6433b49a0ed5e28354d18f2', 'token': 'eXtQhf4KFW3UCoG7SRSVtdranM5BrsNW',
                       'create_time': '1713174740198', 'event_type': 'im.message.receive_v1',
                       'tenant_key': '2cfa3e0dad8cd75d', 'app_id': 'cli_9f6b79a9e737900b'}, 'event': {
            'message': {'chat_id': 'oc_db3dcc0ff9c6d494a07527e363a5861c', 'chat_type': 'p2p',
                        'content': '{"text":"我需要提一个需求！"}', 'create_time': '1713174739807',
                        'message_id': 'om_5b624dce3d5a4ad203e55126668a5ab7', 'message_type': 'text',
                        'update_time': '1713174739807'}, 'sender': {
                'sender_id': {'open_id': 'ou_1a32c82be0a5c6ee7bc8debd75c65e34',
                              'union_id': 'on_0ee3e44cbecb75e4e680bc62eabbebf5',
                              'user_id': 'ecd502d4-2e68-44b5-a25f-f21fd33b1520'}, 'sender_type': 'user',
                'tenant_key': '2cfa3e0dad8cd75d'}}}
    resp = requests.request('POST', headers=headers, url=url, data=json.dumps(data))
    print("\n调用返回结果：", resp.text)
    assert True
