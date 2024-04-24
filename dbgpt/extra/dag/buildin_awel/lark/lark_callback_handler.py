from typing import Dict

from dbgpt.extra.dag.buildin_awel.langgraph.wrappers import lark_api_wrapper


class LarkCallbackHandler:

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def a_handle(self, input_body: Dict) -> Dict:
        print("LarkCallbackHandler_a_handle:", input_body)
        headers = input_body['header']
        event_type = headers['event_type']
        event_id = headers['event_id']
        event = input_body['event']
        rs = lark_api_wrapper.call_lark_api(event)
        print("LarkCallbackHandler_a_handle_result:", rs)
        return rs
