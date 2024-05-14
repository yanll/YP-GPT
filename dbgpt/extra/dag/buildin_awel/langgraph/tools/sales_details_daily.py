import logging
from dbgpt.util.lark import lark_message_util
from dbgpt.extra.dag.buildin_awel.lark import card_templates

from dbgpt.extra.dag.buildin_awel.langgraph.wrappers.crem_30DaysTrx_text import get_crem_30DaysTrx_text



def get_sales_details_daily_card(open_id=None, customer_id=None,conv_id=None):
        da = {
        "list": "list",
        }
        # 发送信息卡片给用户
        lark_message_util.send_card_message(
            receive_id=conv_id,
            content=card_templates.crem_sales_details_content(
                template_variable={
                    "unlike_callback_event": {
                        "event_type": "unlike",
                        "event_source": "crem_30DaysTrx_text_list",
                        "event_data": {
                            "message": "近30天业务表现列表"
                        }
                    },
                    "crem_30DaysTrx_text_list": da["list"]
                }
            )
        )
