from typing import Dict

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
    card = create_card_content_by_template(
        template_id="AAqkIeluuBZF2",
        template_version_name="1.0.5",
        template_variable=template_variable
    )
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


def get_action_index_by_text_from_options(text, options: list) -> int:
    """根据文本选索引，默认返回第一个"""
    for option in options:
        if option["text"] == text:
            return option["action_index"]
    return 1


def get_action_index_by_value_from_options(value, options: list) -> int:
    """根据值选索引，默认返回第一个"""
    for option in options:
        if option["action_value"] == value:
            return option["action_index"]
    return 1


def get_value_by_text_from_options(text, options: list):
    for option in options:
        if option["text"] == text:
            return option["action_value"]
    return ""


def get_text_by_value_from_options(value, options: list):
    for option in options:
        if option["action_value"] == value:
            return option["text"]
    return ""


def card_options_for_requirement_emergency_level() -> list:
    """值必须和飞书项目一致"""
    options = [
        {"action_index": 1, "action_value": "0", "text": "非常紧急"},
        {"action_index": 2, "action_value": "1", "text": "紧急"},
        {"action_index": 3, "action_value": "2", "text": "高"},
        {"action_index": 4, "action_value": "99", "text": "中"},
        {"action_index": 5, "action_value": "1sdyyo6lh", "text": "低"}
    ]
    return options


def card_options_for_requirement_industry_line() -> list:
    """值必须和飞书项目一致"""
    options = [
        {"action_index": 1, "action_value": "662db530cde8ed174622a08d", "text": "航旅行业线"},
        {"action_index": 2, "action_value": "662db56afe2c0b51b33668eb", "text": "大零售行业线"},
        {"action_index": 3, "action_value": "662db596fe2c0b51b33668ec", "text": "线上线下一体化"},
        {"action_index": 4, "action_value": "662db5b688aa18a943e64644", "text": "老板管账"},
        {"action_index": 5, "action_value": "662db5c3a55775e2c9c83bf9", "text": "金融行业线"}
    ]
    return options
