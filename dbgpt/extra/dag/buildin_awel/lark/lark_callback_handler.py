import asyncio
import multiprocessing
import threading
from typing import Dict

from dbgpt.extra.dag.buildin_awel.app.service import AppChatService
from dbgpt.extra.dag.buildin_awel.langgraph.wrappers import lark_callback_handler_wrapper
from dbgpt.util.lark import lark_card_util


class LarkCallbackHandler:

    def __init__(self, **kwargs):
        self.app_chat_service = AppChatService()
        super().__init__(**kwargs)

    def handle(self, input_body: Dict) -> Dict:
        print("LarkCallbackHandler_a_handle:", input_body)
        headers = input_body['header']
        event_type = headers['event_type']
        event_id = headers['event_id']
        event = input_body['event']
        asyncio.create_task(
            lark_callback_handler_wrapper.a_call(self.app_chat_service, event)
        )
        # my_thread = threading.Thread(target=lark_callback_handler_wrapper.a_call, args=(self.app_chat_service, event,))
        # my_thread.daemon = True
        # my_thread.start()
        return {
            "toast": {
                "type": "info",
                "content": "温馨提示",
                "i18n": {
                    "zh_cn": "操作成功！",
                    "en_us": "submitted"
                }
            }
        }
