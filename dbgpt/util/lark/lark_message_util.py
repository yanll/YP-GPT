import json
import logging
from typing import Dict

import requests

from dbgpt.extra.cache.redis_cli import RedisClient
from dbgpt.util import consts
from dbgpt.util.lark.larkutil import build_headers

redis_client = RedisClient()


# 发送消息
def send_message(receive_id: str, content: Dict, receive_id_type: str = "email", msg_type: str = "text",
                 type: str = None):
    url = 'https://open.feishu.cn/open-apis/im/v1/messages'
    params = {
        "receive_id_type": receive_id_type
    }
    data = {
        "receive_id": receive_id,
        "msg_type": msg_type,
        "content": json.dumps(content)
    }
    resp = requests.request('POST', url=url, headers=build_headers(), params=params, data=json.dumps(data),
                            timeout=consts.request_time_out)
    rs = resp.json()
    print('发送消息返回结果：', type, receive_id, resp.json())
    if rs["code"] != 0:
        logging.error("飞书消息发送失败：" + str(rs))
    return rs["data"]


# 发送消息
def send_card_message(receive_id: str, content: Dict):
    return send_message(receive_id, content, "open_id", "interactive", "card_message")


# 发送交互更新卡片
def send_interactive_update_message(token: str, content: Dict):
    url = 'https://open.feishu.cn/open-apis/interactive/v1/card/update'
    data = {
        "token": token,
        "card": content
    }
    resp = requests.request('POST', url=url, headers=build_headers(), data=json.dumps(data),
                            timeout=consts.request_time_out)
    print('发送交互更新卡片返回结果：', resp.json())
    return resp.json()
