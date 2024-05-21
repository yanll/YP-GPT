import logging
from typing import Optional, Type

from langchain.tools import BaseTool
from langchain_core.callbacks import (
    CallbackManagerForToolRun,
)
from pydantic import BaseModel, Field

from dbgpt.extra.dag.buildin_awel.lark import card_templates
from dbgpt.util.lark import larkutil, lark_card_util, lark_message_util


class RequirementCollectInput(BaseModel):
    """
    我要提交一个需求：
    行业线：大零售
    需求内容：在运营后台实现一个数据导出功能。
    期望完成日期：明天
    紧急程度：中
    """
    conv_id: str = Field(
        name="conv_id",
        description="the value of conv_id",
    )
    requirement_content: str = Field(
        name="需求内容",
        description="需求内容",
        default=""
    )
    industry_line: str = Field(
        name="行业线",
        description="行业线：" +
                    lark_card_util.card_options_to_input_field_description(
                        lark_card_util.card_options_for_requirement_industry_line()
                    ),
        default=""
    )
    expected_completion_date: str = Field(
        name="期望完成日期",
        #description="期望完成日期，格式：%Y-%m-%d",
        description="期望完成日期",
        default=""
    )
    emergency_level: str = Field(
        name="紧急程度",
        description="紧急程度，" +
                    lark_card_util.card_options_to_input_field_description(
                        lark_card_util.card_options_for_requirement_emergency_level()
                    ),
        default=""
    )


class RequirementCollectTool(BaseTool):
    name: str = "requirement_collect_tool"
    description: str = (
        "需求收集工具，用于收集需求、痛点。\n"
        "请注意：\n"
        "1、调用本工具需要的参数值来自用户输入，可以默认为空，但是禁止随意编造。\n"
        ""
    )
    args_schema: Type[BaseModel] = RequirementCollectInput

    def _run(
            self,
            conv_id: str = "",
            requirement_content: str = "",
            industry_line: str = "",
            expected_completion_date: str = "",
            emergency_level: str = "",
            run_manager: Optional[CallbackManagerForToolRun] = None,
    ):
        print("开始运行需求收集工具：", conv_id, requirement_content)
        try:
            reuqires = []
            if requirement_content == "":
                reuqires.append("requirement_content")
            if industry_line == "":
                reuqires.append("industry_line")
            if expected_completion_date == "":
                reuqires.append("expected_completion_date")
            if emergency_level == "":
                reuqires.append("emergency_level")
            if len(reuqires) > 0:
                return {"success": "false", "response_message": "the description of " + "[" + ".".join(reuqires) + "]"}
            return handle(
                conv_id=conv_id,
                requirement_content=requirement_content,
                industry_line=industry_line,
                expected_completion_date=expected_completion_date,
                emergency_level=emergency_level
            )
        except Exception as e:
            logging.error("需求收集工具运行异常：" + conv_id + " " + requirement_content, e)
            return repr(e)


def handle(
        conv_id: str = "",
        requirement_content: str = "",
        industry_line: str = "",
        expected_completion_date: str = "",
        emergency_level: str = ""
):
    print("发送飞书需求提报卡片：", conv_id)
    try:
        industry_line_ = lark_card_util.get_action_index_by_text_from_options(
            industry_line,
            lark_card_util.card_options_for_requirement_industry_line()
        )
        industry_line_options_ = lark_card_util.card_options_for_requirement_industry_line()
        emergency_level_ = lark_card_util.get_action_index_by_text_from_options(
            emergency_level,
            lark_card_util.card_options_for_requirement_emergency_level()
        )
        emergency_level_options_ = lark_card_util.card_options_for_requirement_emergency_level()

        return {
            "success": "true",
            "error_message": "",
            "action": {
                "action_name": "send_lark_form_card",
                "card_name": "requirement_collect"
            },
            "data": {
                "conv_id": conv_id,
                "requirement_content": requirement_content,
                "industry_line": industry_line_,
                "industry_line_options": industry_line_options_,
                "expected_completion_date": expected_completion_date,
                "emergency_level": emergency_level_,
                "emergency_level_options": emergency_level_options_
            }
        }
    except Exception as e:
        raise Exception("飞书需求提报数据组装失败：" + conv_id + " " + requirement_content, e)
