from typing import Dict

import requests
import json
import datetime
from dbgpt.extra.dag.buildin_awel.lark import card_templates

from dbgpt.extra.dag.buildin_awel.langgraph.wrappers import lark_api_wrapper


def handle(input_body: Dict):
    headers = input_body['header']
    event_type = headers['event_type']
    event_id = headers['event_id']
    event = input_body['event']
    action = event['action']
    print("call_lark_api:", event_type, event_id, event)
    rs = lark_api_wrapper.call_lark_api(event)
    print("call_lark_api_result:", rs)
    return rs
