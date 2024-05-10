
import logging
from typing import Optional, Type

from langchain.tools import BaseTool
from langchain_core.callbacks import (
    CallbackManagerForToolRun,
)
from pydantic import BaseModel, Field

from dbgpt.extra.dag.buildin_awel.lark import card_templates
from dbgpt.util.lark import larkutil, lark_card_util


class RequirementSearchToolInput(BaseModel):
    conv_id: str = Field(
        name="conv_id",
        description="the value of conv_id",
    )
    industry_line: str = Field(
        name="行业线",
        description="行业线，" +
                    lark_card_util.card_options_to_input_field_description(
                        lark_card_util.card_options_for_requirement_industry_line()
                    ),
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
    requirement_create_name: str = Field(
        name="需求创建者名称", description="需求创建者名称", default="")


class RequirementSearchTool(BaseTool):
    name: str = "requirement_search_tool"
    description: str = (
        "你是一个需求信息查询工具，用于需求查询，结果准确、可信。 "
        "当你需要通过调用工具查询需求信息时非常有用。 "
        "输入参数应该是工具需要的全部参数。"
        "调用本工具需要的参数值均来自用户的输入，可以默认为空，但是禁止随意编造。"
        "请将查询结果数据整理并美化后输出。"

    )
    max_results: int = 20
    args_schema: Type[BaseModel] = RequirementSearchToolInput

    def _run(
            self,
            conv_id: str = "",
            industry_line: str = "",
            emergency_level: str = "",
            requirement_create_name: str = "",
            run_manager: Optional[CallbackManagerForToolRun] = None,
    ):
        """Use the tool."""
        print("开始执行日报信息查询工具：", conv_id, industry_line,emergency_level,requirement_create_name, self.max_results)
        try:
            if industry_line == "":
                resp = {"success": "false", "response_message": "the description of industry_line"}
            elif emergency_level == "":
                resp = {"success": "false", "response_message": "the description of emergency_level"}
            elif requirement_create_name == "":
                resp = {"success": "false", "response_message": "the description of requirement_create_name"}

            else:
                resp = do_collect(
                    conv_id=conv_id,
                    industry_line=industry_line,
                    emergency_level=emergency_level,
                    requirement_create_name=requirement_create_name
                )
            return resp
        except Exception as e:
            logging.error("工具运行异常：", e)
            return repr(e)

def do_collect(
        conv_id: str = "",
        industry_line: str = "",
        emergency_level: str = "",
        requirement_create_name: str = ""
    ):
    print("发送飞书需求提报卡片：", conv_id)
    try:
        """

        """

        larkutil.send_message(
            receive_id=conv_id,
            content=card_templates.requirement_search_card_content(
                template_variable={
                    "card_metadata": {
                        "card_name": "requirement_search",
                        "description": "需求查询表单"
                    },
                    "industry_line": lark_card_util.get_action_index_by_text_from_options(
                        industry_line,
                        lark_card_util.card_options_for_requirement_industry_line()
                    ),
                    "industry_line_options": lark_card_util.card_options_for_requirement_industry_line(),
                    "emergency_level": lark_card_util.get_action_index_by_text_from_options(
                        emergency_level,
                        lark_card_util.card_options_for_requirement_emergency_level()
                    ),
                    "emergency_level_options": lark_card_util.card_options_for_requirement_emergency_level(),
                    "requirement_create_name": requirement_create_name,

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
        "display_type": "form",
        "data": {
            "conv_id": conv_id,
            "industry_line": industry_line,
            "requirement_create_name": requirement_create_name,
            "emergency_level": emergency_level
        }
    }