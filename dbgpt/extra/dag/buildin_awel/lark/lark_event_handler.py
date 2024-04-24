from typing import Dict

import requests
import json
import datetime

from dbgpt.extra.cache.redis_cli import RedisClient
from dbgpt.extra.dag.buildin_awel.lark import card_templates

from dbgpt.extra.dag.buildin_awel.langgraph.wrappers import lark_api_wrapper


def valid_event_type(input_body: Dict):
    headers = input_body["header"]
    event_type = headers["event_type"]

    if (event_type == "p2p_chat_create"):
        print("机器人会话被创建", input_body)
    if (event_type == "im.chat.member.bot.added_v1"):
        print("机器人进群了", input_body)
    if (event_type == "im.chat.member.bot.deleted_v1"):
        print("机器人被群踢了", input_body)

    if (event_type in ["im.message.receive_v1",
                       "p2p_chat_create",
                       "im.chat.member.bot.added_v1",
                       "im.chat.member.bot.deleted_v1"
                       ]):
        return True
    return False


def valid_repeat(redis_client: RedisClient, input_body: Dict):
    headers = input_body["header"]
    event_id = headers["event_id"]
    redis_key = "lark_event_id_for_no_repeat_" + event_id
    exists: str = redis_client.get(redis_key)
    if (exists == "true"):
        print("飞书事件已经存在，跳过执行：", input_body)
        return False
    redis_client.set(redis_key, "true", 12 * 60 * 60)
    return True
