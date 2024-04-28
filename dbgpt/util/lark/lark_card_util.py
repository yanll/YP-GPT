import json
from typing import Dict

import requests

from dbgpt.util.lark import larkutil


def send_message_with_bingo(receive_id: str, template_variable: Dict):
    """包含点赞、新会话功能的消息卡片"""
    card = create_card_content_by_template("AAqkIdjGltfge", "1.0.4", template_variable)
    larkutil.send_message(
        receive_id=receive_id,
        receive_id_type="open_id",
        content=card,
        msg_type="interactive"
    )
def send_message_with_welcome(receive_id: str, template_variable: Dict):
    """欢迎卡片"""
    card = create_card_content_by_template("AAqkIeluuBZF2", "1.0.4", template_variable)
    larkutil.send_message(
        receive_id=receive_id,
        receive_id_type="open_id",
        content=card,
        msg_type="interactive"
    )


def create_card_content_by_template(template_id: str, template_version_name: str, template_variable: Dict):
    """"""
    card = {
        "type": "template",
        "data": {
            "template_id": template_id, "template_version_name": template_version_name,
            "template_variable": template_variable
        }
    }
    return card


def card_option2str(options: list):
    options_str = str(len(options)) + '个选项：'
    for option in options:
        options_str += option['text'] + "、"
    return options_str[:-1]

def card_option2dict(options: list):
    options_dict = {}
    for idx, option in enumerate(options):
        options_dict[option['text']] = idx + 1
    return options_dict

