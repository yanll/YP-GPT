import json
import logging
from typing import Optional, Type

from langchain.tools import BaseTool
from langchain_core.callbacks import (
    CallbackManagerForToolRun,
)
from pydantic import BaseModel, Field

from dbgpt.extra.dag.buildin_awel.lark import card_templates
from dbgpt.util.lark import larkutil, lark_card_util, lark_message_util


class ConvIdInput(BaseModel):
    conv_id: str = Field(
        name="conv_id",
        description="the value of conv_id",
    )

class AbilityDisplayTool(BaseTool):
    name: str = "ability_display_tool"
    description: str = (
        "这是一个展示能力的工具。\n"
        "当用户询问有什么能力时，调用此工具。\n"
        "触发条件可以是'你有什么能力'、‘你会什么’等关键词。\n"
    )
    args_schema: Type[BaseModel] = ConvIdInput

    def _run(
            self,
            conv_id: str = "",
    ):
        print("开始调用能力卡片：", conv_id)
        try:
            nickname = ""
            userinfo = larkutil.select_userinfo(open_id=conv_id)
            if userinfo and "name" in userinfo:
                nickname = userinfo["name"] + " "
            content = card_templates.welcome_and_ability_display(
                template_variable={
                    "card_metadata": {
                        "card_name": "ability_display",
                        "description": "展示能力"
                    },
                    "message_content": "已开启新会话！",
                    "current_nickname": nickname
                }
            )

            return {
                "success": "true",
                "error_message": "",
                "action": {
                    "action_name": "send_lark_form_card",
                    "card_name": "ability_display",
                },
                "data": {
                    "conv_id": conv_id,
                    "content": content
                }
            }
        except Exception as e:
            logging.error("能力卡片异常：" + conv_id , e)
            return '能力卡片异常'

