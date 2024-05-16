import json
import logging
from typing import Dict

import requests

from dbgpt.extra.cache.redis_cli import RedisClient
from dbgpt.util import consts
from dbgpt.util.lark.larkutil import build_headers, build_headers_rag

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
        return "飞书消息发送失败：" + str(rs)
    return rs["data"]


# 发送消息
def send_card_message(receive_id: str, content: Dict):
    return send_message(receive_id, content, "open_id", "interactive", "card_message")


def send_message_rag(receive_id: str, content: Dict, receive_id_type: str = "email", msg_type: str = "text",
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
    resp = requests.request('POST', url=url, headers=build_headers_rag(), params=params, data=json.dumps(data))
    rs = resp.json()
    print('发送消息返回结果：', type, receive_id, resp.json())
    if rs["code"] != 0:
        logging.error("飞书消息发送失败：" + str(rs))
    return rs["data"]


def send_card_message_rag(receive_id: str, content: Dict):
    return send_message_rag(receive_id, content, "open_id", "interactive", "card_message")


# 发送应用发送的卡片消息
def send_interactive_update_message(open_id: str, token: str, content: Dict):
    url = 'https://open.feishu.cn/open-apis/interactive/v1/card/update'
    content['open_ids'] = [open_id]
    data = {
        "token": token,
        "card": content
    }
    resp = requests.request('POST', url=url, headers=build_headers(), data=json.dumps(data),
                            timeout=consts.request_time_out)
    print('发送交互更新卡片返回结果：', resp.json())
    return resp.json()


# 发送交互更新卡片
def update_interactive_card_rag(message_id, content: Dict):
    url = "https://open.feishu.cn/open-apis/im/v1/messages/{}".format(message_id)
    data = {
        "content": json.dumps(content)
    }

    resp = requests.patch(url=url, headers=build_headers_rag(), json=data)

    print('发送交互更新卡片返回结果：', resp.json())
    return resp.json()


def send_loading_message_rag(receive_id):
    resp_data = send_message_rag(receive_id=receive_id, content=resp_loading_hint, receive_id_type='open_id',
                                 msg_type='interactive', type='card_message')
    return resp_data['message_id']


def update_loading_message_rag(message_id, type='standard'):
    resp_placeholder = None
    if type == 'standard':
        resp_placeholder = resp_standard_hint
    elif type == 'error':
        resp_placeholder = resp_error_hint
    res = update_interactive_card_rag(message_id=message_id, content=resp_placeholder)
    return res


resp_loading_hint = {
    "config": {},
    "i18n_elements": {
        "zh_cn": [
            {
                "tag": "column_set",
                "flex_mode": "none",
                "background_style": "default",
                "horizontal_spacing": "4px",
                "horizontal_align": "center",
                "columns": [
                    {
                        "tag": "column",
                        "width": "30px",
                        "vertical_align": "center",
                        "background_style": "default",
                        "elements": [
                            {
                                "tag": "img",
                                "img_key": "img_v3_02at_d325ba34-7bb2-4b80-977b-8092ebaf29dg",
                                "preview": False,
                                "transparent": True,
                                "scale_type": "crop_center",
                                "size": "stretch",
                                "alt": {
                                    "tag": "plain_text",
                                    "content": ""
                                }
                            }
                        ]
                    },
                    {
                        "tag": "column",
                        "width": "weighted",
                        "vertical_align": "center",
                        "background_style": "default",
                        "elements": [
                            {
                                "tag": "column_set",
                                "flex_mode": "none",
                                "horizontal_spacing": "default",
                                "background_style": "default",
                                "columns": [
                                    {
                                        "tag": "column",
                                        "elements": [
                                            {
                                                "tag": "div",
                                                "text": {
                                                    "tag": "plain_text",
                                                    "content": "正在使用企业知识库回答",
                                                    "text_size": "normal",
                                                    "text_align": "left",
                                                    "text_color": "default"
                                                }
                                            }
                                        ],
                                        "width": "weighted",
                                        "weight": 1
                                    }
                                ]
                            }
                        ],
                        "weight": 1
                    }
                ],
                "margin": "0px 0px 0px 0px"
            }
        ]
    },
    "i18n_header": {}
}

resp_standard_hint = {
    "config": {},
    "i18n_elements": {
        "zh_cn": [
            {
                "tag": "column_set",
                "flex_mode": "none",
                "horizontal_spacing": "default",
                "background_style": "default",
                "columns": [
                    {
                        "tag": "column",
                        "elements": [
                            {
                                "tag": "div",
                                "text": {
                                    "tag": "plain_text",
                                    "content": "已经根据企业知识库生成答案！",
                                    "text_size": "normal",
                                    "text_align": "left",
                                    "text_color": "default"
                                }
                            }
                        ],
                        "width": "weighted",
                        "weight": 1
                    }
                ]
            }
        ]
    },
    "i18n_header": {}
}

resp_error_hint = {
    "config": {},
    "i18n_elements": {
        "zh_cn": [
            {
                "tag": "column_set",
                "flex_mode": "none",
                "horizontal_spacing": "default",
                "background_style": "default",
                "columns": [
                    {
                        "tag": "column",
                        "elements": [
                            {
                                "tag": "div",
                                "text": {
                                    "tag": "plain_text",
                                    "content": "生成失败！",
                                    "text_size": "normal",
                                    "text_align": "left",
                                    "text_color": "default"
                                }
                            }
                        ],
                        "width": "weighted",
                        "weight": 1
                    }
                ]
            }
        ]
    },
    "i18n_header": {}
}
