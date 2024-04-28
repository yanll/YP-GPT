import logging
from typing import Optional, Type

from langchain.tools import BaseTool
from langchain_core.callbacks import (
    CallbackManagerForToolRun,
)
from pydantic import BaseModel, Field

from dbgpt.extra.dag.buildin_awel.lark import card_templates
from dbgpt.util.lark import larkutil
from dbgpt.util.lark.lark_card_util import card_option2str, card_option2dict

# emergency_level_options = [
#     {"text": "P0高", "action_value": "0"},
#     {"text": "P1中", "action_value": "1"},
#     {"text": "P2低", "action_value": "2"},
#     {"text": "待定", "action_value": "99"}
# ]

emergency_level_options = [
  {
    "text": "非常紧急",
    "action_value": "s0"
  },
  {
    "text": "紧急",
    "action_value": "s1"
  },
  {
    "text": "高",
    "action_value": "s2"
  },
  {
    "text": "中",
    "action_value": "s99"
  },
  {
    "text": "低",
    "action_value": "1sdyyo6lh"
  }
]


class RequirementCollectInput(BaseModel):
    """

    """
    conv_id: str = Field(
        name="conv_id",
        description="value of conv_id",
        default=""
    )
    requirement_content: str = Field(
        name="需求内容",
        description="需求内容",
        default=""
    )
    expected_completion_date: str = Field(
        name="期望完成日期",
        description="期望完成日期，格式：%Y-%m-%d",
        default=""
    )
    emergency_level: str = Field(
        name="紧急程度",
        description="描述紧急程度，" + card_option2str(emergency_level_options),
        default=""
    )


class RequirementCollectTool(BaseTool):
    name: str = "requirement_collect_tool"
    description: str = (
        "这是一个需求收集工具，用于收集用户工作中的需求、对某个事物的要求、或其他痛点等信息"
        "当需要收集需求数据时非常有用。 "
        "能够尽可能全的收集需求信息。"
        "调用本工具需要的参数值均来自用户的输入，可以默认为空，但是禁止随意编造。"
        ""
    )
    args_schema: Type[BaseModel] = RequirementCollectInput

    def _run(
            self,
            conv_id: str = "",
            requirement_content: str = "",
            expected_completion_date: str = "",
            emergency_level: str = "",
            run_manager: Optional[CallbackManagerForToolRun] = None,
    ):
        """Use the tool."""
        print("开始运行需求收集工具：", conv_id, requirement_content, emergency_level, expected_completion_date)
        try:
            if requirement_content == "":
                resp = {"success": "false", "response_message": "the description of requirement_content"}
            elif expected_completion_date == "":
                resp = {"success": "false", "response_message": "the description of expected_completion_date"}
            elif emergency_level == "":
                resp = {"success": "false", "response_message": "the description of emergency_level"}
            else:
                resp = do_collect(
                    conv_id=conv_id,
                    requirement_content=requirement_content,
                    expected_completion_date=expected_completion_date,
                    emergency_level=emergency_level
                )
            return resp
        except Exception as e:
            logging.error("工具运行异常：", e)
            return repr(e)


def do_collect(
        conv_id: str = "",
        requirement_content: str = "",
        expected_completion_date: str = "",
        emergency_level: str = ""
):
    print("发送飞书需求提报卡片：", conv_id)
    try:
        """
        我要提交一个需求：
        需求内容：在运营后台实现一个数据导出功能。
        期望完成日期：2024-05-20
        紧急程度：P0
        """
        emergency_level2dict = card_option2dict(emergency_level_options)

        larkutil.send_message(
            receive_id=conv_id,
            content=card_templates.create_requirement_card_content(
                template_variable={
                    "card_metadata": {
                        "card_name": "requirement_collect",
                        "description": "需求收集表单"
                    },
                    "requirement_content": requirement_content,
                    "expected_completion_date": expected_completion_date,
                    "emergency_level": emergency_level2dict[emergency_level] if emergency_level in emergency_level2dict else 1,
                    "emergency_level_options": emergency_level_options
                }
            ),
            receive_id_type="open_id",
            msg_type="interactive"
        )
    except Exception as e:
        logging.error("飞书需求提报卡片发送失败：", e)

    return {
        "success": "true",
        "error_message": "",
        "data": {
            "conv_id": conv_id,
            "requirement_content": requirement_content,
            "expected_completion_date": expected_completion_date,
            "emergency_level": emergency_level
        }
    }
