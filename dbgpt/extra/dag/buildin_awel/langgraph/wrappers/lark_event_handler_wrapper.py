import json
import logging
import uuid
from typing import Dict

from langchain_core.agents import AgentFinish

from dbgpt.extra.dag.buildin_awel.app.service import AppChatService
from dbgpt.extra.dag.buildin_awel.lark import card_templates, lark_card_handler
from dbgpt.util.lark import lark_card_util, lark_message_util


class LarkEventHandlerWrapper:

    def __init__(self, **kwargs):
        self.app_chat_service = AppChatService()
        super().__init__(**kwargs)

    def a_reply(self, sender_open_id: str, human_message: str, assistant_response):
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
                        if last_output_str.startswith("Exception"):
                            logging.error("上一步节点执行异常：" + last_output_str)
                        elif len(last_output_str) > 0:
                            # TODO-YLL-FIXME 查询我的周报复现
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
        if data is None:
            return
        card_name = action["card_name"]
        if card_name == "requirement_collect":
            resp = lark_message_util.send_card_message(
                receive_id=sender_open_id,
                content=card_templates.create_requirement_card_content(
                    template_variable={
                        "submit_callback_event": {
                            "event_type": "submit",
                            "event_source": card_name
                        },
                        "unlike_callback_event": {
                            "event_type": "unlike",
                            "event_source": card_name,
                            "event_data": {
                                "message": "需求收集表单"
                            }
                        },
                        "ai_message": resp_msg,
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
        if card_name == "crm_bus_customer_collect":
            resp = lark_message_util.send_card_message(
                receive_id=sender_open_id,
                content=data['content']
            )
            lark_message_id = resp["message_id"]
            self.store_his_message(sender_open_id, resp_msg, "form_card", lark_message_id)
            return
        if card_name == "crm_bus_customer_query_result":
            resp = lark_message_util.send_card_message(
                receive_id=sender_open_id,
                content=data['content']
            )
            lark_message_id = resp["message_id"]
            self.store_his_message(sender_open_id, resp_msg, "form_card", lark_message_id)
            return
        if card_name == "ability_display":
            resp = lark_message_util.send_card_message(
                receive_id=sender_open_id,
                content=data['content']
            )
            lark_message_id = resp["message_id"]
            self.store_his_message(sender_open_id, resp_msg, "form_card", lark_message_id)
            return
        if card_name == "daily_report_collect":
            resp = lark_message_util.send_card_message(
                receive_id=sender_open_id,
                # content=card_templates.create_daily_report_card_content(
                #     template_variable={
                #         "card_metadata": {
                #             "card_name": card_name,
                #             "card_description": "日报收集表单"
                #         },
                #         "submit_callback_event": {
                #             "event_type": "submit",
                #             "event_source": card_name
                #         },
                #         "unlike_callback_event": {
                #             "event_type": "unlike",
                #             "event_source": card_name,
                #             "event_data": {
                #                 "message": "需求收集表单"
                #             }
                #         },
                #         "ai_message": resp_msg,
                #         "daily_report_content": data["daily_report_content"],
                #         "create_date": data["create_date"],
                #         "daily_report_tomorrow_plans": data["daily_report_tomorrow_plans"]
                #     }
                # )
                content=lark_card_handler.get_lard_card_json(
                    card_name='daily_report',
                    template_variable={
                        "card_metadata": {
                            "card_name": card_name,
                            "card_description": "日报收集表单"
                        },
                        "submit_callback_event": {
                            "event_type": "submit",
                            "event_source": card_name
                        },
                        "unlike_callback_event": {
                            "event_type": "unlike",
                            "event_source": card_name,
                            "event_data": {
                                "message": "日报收集表单"
                            }
                        },
                        "ai_message": resp_msg,
                        "daily_report_content": data["daily_report_content"],
                        "create_date": data["create_date"],
                        "daily_report_tomorrow_plans": data["daily_report_tomorrow_plans"]
                    }

                )
            )
            lark_message_id = resp["message_id"]
            self.store_his_message(sender_open_id, resp_msg, "form_card", lark_message_id)
            return
        if card_name == "weekly_report_collect":
            resp = lark_message_util.send_card_message(
                receive_id=sender_open_id,
                content=card_templates.create_weekly_report_card_content(
                    template_variable={
                        "card_metadata": {
                            "card_name": card_name,
                            "card_description": "周报收集表单"
                        },
                        "submit_callback_event": {
                            "event_type": "submit",
                            "event_source": card_name
                        },
                        "unlike_callback_event": {
                            "event_type": "unlike",
                            "event_source": card_name,
                            "event_data": {
                                "message": "需求收集表单"
                            }
                        },
                        "ai_message": resp_msg,
                        "weekly_report_next_week_plans": data["weekly_report_next_week_plans"],
                        "create_date": data["create_date"],
                        "weekly_report_client": "",
                        "weekly_report_content": data["weekly_report_content"]
                    }
                )
            )
            lark_message_id = resp["message_id"]
            self.store_his_message(sender_open_id, resp_msg, "form_card", lark_message_id)
            return
        if card_name == "customer_visit_record_collect":
            resp = lark_message_util.send_card_message(
                receive_id=sender_open_id,
                content=card_templates.create_customer_visit_record_card_content(
                    template_variable={
                        "card_metadata": {
                            "card_name": card_name,
                            "card_description": "拜访收集表单"
                        },
                        "submit_callback_event": {
                            "event_type": "submit",
                            "event_source": card_name
                        },
                        "unlike_callback_event": {
                            "event_type": "unlike",
                            "event_source": card_name,
                            "event_data": {
                                "message": "跟进拜访表单"
                            }
                        },
                        "ai_message": resp_msg,
                        "customer_name": data["customer_name"],
                        "visit_content": data["visit_content"],
                        "contacts": data["contacts"],
                        "visit_date": data["visit_date"],
                        "visit_method": data["visit_method"],
                        "visit_methods": data["visit_methods"],
                        "visit_type": data["visit_type"],
                        "visit_types": data["visit_types"]
                    }
                )
            )
            lark_message_id = resp["message_id"]
            self.store_his_message(sender_open_id, resp_msg, "form_card", lark_message_id)
            return
        if card_name == "merchant_list_card":
            resp = lark_message_util.send_card_message(
                receive_id=sender_open_id,
                content=card_templates.create_merchant_list_card_content(
                    template_variable={
                        "unlike_callback_event": {
                            "event_type": "unlike",
                            "event_source": card_name,
                            "event_data": {
                                "message": "商户信息列表"
                            }
                        },
                        "query_str": data["query_str"],
                        "sales_diapaly": data["sales_diapaly"],
                        "merchant_list": data["list"]
                    }
                )
            )
            lark_message_id = resp["message_id"]
            self.store_his_message(sender_open_id, resp_msg, "form_card", lark_message_id)
            return
        if card_name == "daily_report_list_card":
            resp = lark_message_util.send_card_message(
                receive_id=sender_open_id,
                content=card_templates.create_search_daily_report_card_content(
                    template_variable={
                        "unlike_callback_event": {
                            "event_type": "unlike",
                            "event_source": card_name,
                            "event_data": {
                                "message": "日报信息列表"
                            }
                        },
                        "query_str": data["query_str"],
                        "daily_report_list": data["list"]
                    }
                )
            )
            lark_message_id = resp["message_id"]
            self.store_his_message(sender_open_id, resp_msg, "form_card", lark_message_id)
            return
        if card_name == "requirement_search_list":
            resp = lark_message_util.send_card_message(
                receive_id=sender_open_id,
                content=card_templates.create_requirement_search_list_card_content(
                    template_variable={
                        "unlike_callback_event": {
                            "event_type": "unlike",
                            "event_source": card_name,
                            "event_data": {
                                "message": "需求信息列表"
                            }
                        },
                        "query_str": data["query_str"],
                        "requirement_search_list": data["list"]
                    }
                )
            )
            lark_message_id = resp["message_id"]
            self.store_his_message(sender_open_id, resp_msg, "form_card", lark_message_id)
            return

        if card_name == "crem_30DaysTrx_text_list":
            resp = lark_message_util.send_card_message(
                receive_id=sender_open_id,
                content=card_templates.crem_30DaysTrx_text_content(
                    template_variable={
                        "unlike_callback_event": {
                            "event_type": "unlike",
                            "event_source": card_name,
                            "event_data": {
                                "message": "近30天业务表现列表"
                            }
                        },
                        "query_str": data["query_str"],
                        "crem_30DaysTrx_text_list": data["list"]
                    }
                )
            )
            lark_message_id = resp["message_id"]
            self.store_his_message(sender_open_id, resp_msg, "form_card", lark_message_id)
            return

        if card_name == "daily_push_message_list_card":
            resp = lark_message_util.send_card_message(
                receive_id=sender_open_id,
                content=card_templates.crem_sales_details_content(
                    template_variable={
                        "unlike_callback_event": {
                            "event_type": "unlike",
                            "event_source": card_name,
                            "event_data": {
                                "message": "人员分级销售详情展示"
                            }
                        },
                        "query_str": data["query_str"],
                        "daily_push_message_list": data["list"],
                        "sales_diapaly": data["sales_diapaly"]
                    }
                )
            )
            lark_message_id = resp["message_id"]
            self.store_his_message(sender_open_id, resp_msg, "form_card", lark_message_id)
            return

        if card_name == "feedback_collect":
            resp = lark_message_util.send_card_message(
                receive_id=sender_open_id,
                content=card_templates.create_feedback_card_content(
                    template_variable={
                        "submit_callback_event": {
                            "event_type": "submit",
                            "event_source": "feedback_collect",
                            "event_data": {
                                "original_message_id": ""
                            }
                        },
                        "message": "",
                        "feedback": data["feedback"],
                        "effect": data["effect"],
                        "recommendation": data["recommendation"],
                        "reference_url": data["reference_url"]
                    }
                )
            )
            return

        if card_name == "knowledge_result":
            answer_from_knowledge = data["answer_from_knowledge"]
            answer_from_general_ai = data["answer_from_general_ai"]
            answer = (
                    "\n\n*以下是知识库检索内容：*\n" + answer_from_knowledge +
                    "\n\n*以下是通用AI回复内容：*\n" + answer_from_general_ai +
                    "\n\n*以下是结合内容：*\n" + resp_msg
            )
            resp = lark_card_util.send_message_with_bingo(
                receive_id=sender_open_id,
                template_variable={
                    "message_content": "",
                    "muti_text": answer,
                    "unlike_callback_event": {
                        "event_type": "unlike",
                        "event_source": "knowledge_result_card",
                        "event_data": {
                            "message": answer
                        }
                    }
                }
            )
            self.store_his_message(sender_open_id, answer, "text", resp["message_id"])
            return

    def lark_reply_general_message(self, sender_open_id, resp_msg):
        resp = lark_card_util.send_message_with_bingo(
            receive_id=sender_open_id,
            template_variable={
                "unlike_callback_event": {
                    "event_type": "unlike",
                    "event_source": "general_card",
                    "event_data": {
                        "message": resp_msg
                    }
                },
                "message_content": resp_msg
            }
        )
        lark_message_id = resp["message_id"]
        self.store_his_message(sender_open_id, resp_msg, "text", lark_message_id)
