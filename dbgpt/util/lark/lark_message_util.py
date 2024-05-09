import json
from typing import Dict

import requests

from dbgpt.extra.cache.redis_cli import RedisClient
from dbgpt.util.lark.larkutil import build_headers

redis_client = RedisClient()


# 发送消息
def send_message(receive_id: str, content: Dict, receive_id_type: str = "email", msg_type: str = "text"):
    url = 'https://open.feishu.cn/open-apis/im/v1/messages'
    params = {
        "receive_id_type": receive_id_type
    }
    data = {
        "receive_id": receive_id,
        "msg_type": msg_type,
        "content": json.dumps(content)
    }
    resp = requests.request('POST', url=url, headers=build_headers(), params=params, data=json.dumps(data))
    print('发送消息返回结果：', resp.json())
    return resp.json()


# 发送交互更新卡片
def send_interactive_update_message(token: str, content: Dict):
    url = 'https://open.feishu.cn/open-apis/interactive/v1/card/update'
    data = {
        "token": token,
        "card": content
    }
    resp = requests.request('POST', url=url, headers=build_headers(), data=json.dumps(data))
    print('发送交互更新卡片返回结果：', resp.json())
    return resp.json()
