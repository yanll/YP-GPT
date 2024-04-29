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
            lark_callback_handler_wrapper.a_call(event)
        )
        # my_thread = threading.Thread(target=lark_callback_handler_wrapper.a_call, args=(event,))
        # my_thread.daemon = True
        # my_thread.start()
        # # process = multiprocessing.Process(target=lark_callback_handler_wrapper.a_call, args=(event,))
        # # process.daemon = True
        # # process.start()
        print("回复需求卡片交互")
        operator = event['operator']
        open_id = operator['open_id']
        if "action" in event:
            action = event['action']
            action_value = action['value']
            if action_value == "like":
                return {
                    "toast": {
                        "type": "info",
                        "content": "温馨提示",
                        "i18n": {
                            "zh_cn": "感谢您的点赞！",
                            "en_us": "submitted"
                        }
                    }
                }
            if action_value == "unlike":
                return {
                    "toast": {
                        "type": "info",
                        "content": "温馨提示",
                        "i18n": {
                            "zh_cn": "感谢您的反馈，我们会努力改进哦！",
                            "en_us": "submitted"
                        }
                    }
                }
            if action_value == "new_chat":
                asyncio.create_task(
                    self.app_chat_service.a_disable_app_chat_his_message_by_uid(open_id)
                )
                lark_card_util.send_message_with_welcome(
                    receive_id=open_id,
                    template_variable={
                        "message_content": "已开启新会话！"
                    }
                )
                return {}
        print("需求交互操作成功")
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
