from typing import Dict

from dbgpt.extra.dag.buildin_awel.langgraph.wrappers import lark_api_wrapper


class LarkCallbackHandler:

    async def a_handle(self, input_body: Dict) -> Dict:
        headers = input_body['header']
        event_type = headers['event_type']
        event_id = headers['event_id']
        event = input_body['event']
        print("call_lark_api:", event_type, event_id, event)
        rs = lark_api_wrapper.call_lark_api(event)
        print("call_lark_api_result:", rs)
        return rs

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
