from typing import Dict, List

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


def card_options_to_input_field_description(options: list) -> str:
    """将卡片选项转换为参数接收字段中的选项描述"""
    options_str = "共" + str(len(options)) + "个选项："
    for option in options:
        options_str += option['text'] + "、"
    rs = options_str[:-1]
    print("卡片选项转换结果：", rs)
    return rs


def card_options_to_dict_for_value_bind(options: list) -> Dict:
    """将卡片选项转换为可以绑定回填值的字典"""
    options_dict = {}
    for idx, option in enumerate(options):
        options_dict[option['text']] = idx + 1
    print("飞书卡片选项字典：", options_dict)
    return options_dict


def get_value_by_text_from_options(text, options: list):
    for option in options:
        if option["text'"] == text:
            return option["action_value"]
    return ""


def get_text_by_value_from_options(value, options: list):
    for option in options:
        if option['action_value'] == value:
            return option["text"]
    return ""


def card_options_for_requirement_emergency_level(options: list) -> list:
    options = [
        {
            "action_value": "L1",
            "text": "非常紧急"
        },
        {
            "action_value": "L2",
            "text": "紧急"
        },
        {
            "action_value": "L3",
            "text": "高"
        },
        {
            "action_value": "L4",
            "text": "中"},
        {
            "action_value": "L5",
            "text": "低"
        }
    ]
    return options
