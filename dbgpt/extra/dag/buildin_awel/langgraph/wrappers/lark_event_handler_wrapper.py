import json
import logging
import uuid
from typing import Dict

from langchain_core.agents import AgentFinish

from dbgpt.extra.dag.buildin_awel.app.service import AppChatService
from dbgpt.extra.dag.buildin_awel.lark import card_templates
from dbgpt.util.lark import lark_card_util, lark_message_util


class LarkEventHandlerWrapper:

    def __init__(self, **kwargs):
        self.app_chat_service = AppChatService()
        super().__init__(**kwargs)

    async def a_reply(self, sender_open_id: str, human_message: str, assistant_response):
        resp_msg = str(assistant_response)
        action = None
        data = None
        if isinstance(assistant_response, Dict):
            agent_outcome = assistant_response['agent_outcome']
            if isinstance(agent_outcome, AgentFinish):
                return_values = agent_outcome.return_values
                resp_msg = return_values['output']
                if "last_output" in return_values:
                    last_output_str = return_values["last_output"]
                    try:
                        if len(last_output_str) > 0:
                            last_output = json.loads(last_output_str.replace("'", "\""))
                            if last_output and "action" in last_output:
                                action = last_output["action"]
                            if last_output and "data" in last_output:
                                data = last_output["data"]
                    except Exception as e:
                        logging.error("last_output_load_err：", last_output_str)
        print("lark_event_handler_wrapper_reply", resp_msg)

        if action is not None:
            action_name = action["action_name"]
            if action_name == "send_lark_form_card":
                self.lark_reply_form_card_message(sender_open_id, resp_msg, action, data)
                return
        self.lark_reply_general_message(sender_open_id, resp_msg)

    def store_his_message(self, sender_open_id, content, display_type, lark_message_id):
        rec = {
            "id": str(uuid.uuid1()),
            "agent_name": "SalesAssistant",
            "node_name": "final",
            "conv_uid": sender_open_id,
            "message_type": "view",
            "content": content,
            "message_detail": "",
            "display_type": display_type,
            "lark_message_id": lark_message_id
        }
        self.app_chat_service.add_app_chat_his_message(rec)

    def lark_reply_form_card_message(self, sender_open_id: str, resp_msg: str, action: Dict, data: Dict):
        card_name = action["card_name"]
        if card_name == "requirement_collect":
            resp = lark_message_util.send_card_message(
                receive_id=sender_open_id,
                content=card_templates.create_requirement_card_content(
                    template_variable={
                        "card_metadata": {
                            "card_name": card_name,
                            "description": "需求收集表单"
                        },
                        "requirement_content": data["requirement_content"],
                        "industry_line": data["industry_line"],
                        "industry_line_options": data["industry_line_options"],
                        "expected_completion_date": data["expected_completion_date"],
                        "emergency_level": data["emergency_level"],
                        "emergency_level_options": data["emergency_level_options"]
                    }
                )
            )
            lark_message_id = resp["message_id"]
            self.store_his_message(sender_open_id, resp_msg, "form_card", lark_message_id)
            return

    def lark_reply_general_message(self, sender_open_id, resp_msg):
        resp = lark_card_util.send_message_with_bingo(
            receive_id=sender_open_id,
            template_variable={
                "message_content": resp_msg
            }
        )
        lark_message_id = resp["message_id"]
        self.store_his_message(sender_open_id, resp_msg, "text", lark_message_id)
