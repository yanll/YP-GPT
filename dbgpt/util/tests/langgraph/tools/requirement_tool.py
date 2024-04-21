from typing import Dict, Optional, Type

from langchain.tools import BaseTool
from langchain_core.callbacks import (
    CallbackManagerForToolRun,
)
from pydantic import BaseModel, Field


class RequirementCollectInput(BaseModel):
    """

    """
    requirement_content: str = Field(
        name="需求内容",
        description="需求内容"
        # description="需求内容：默认为空，必须从用户输入的信息中提取，禁止编造。"
    )
    expected_completion_time: str = Field(
        name="期望完成时间",
        description="期望完成时间"
        # description="期望完成时间：默认为空，必须从用户输入的信息中提取，禁止编造。"
    )
    emergency_level: str = Field(name="紧急程度", description="紧急程度", default="")


class RequirementCollectTool(BaseTool):
    name: str = "requirement_collect_tool"
    description: str = (
        "这是一个需求收集工具，用于收集用户工作中的需求、对某个事物的要求、或其他痛点等信息"
        "当需要收集需求数据时非常有用。 "
        "能够尽可能全的收集需求信息。"
        ""
    )
    args_schema: Type[BaseModel] = RequirementCollectInput

    def _run(
            self,
            requirement_content: str,
            expected_completion_time: str,
            emergency_level: str = "P0",
            run_manager: Optional[CallbackManagerForToolRun] = None,
    ):
        """Use the tool."""
        print("开始执行需求收集工具：", requirement_content, emergency_level, expected_completion_time)
        try:
            if requirement_content == "":
                resp = {"success": "false", "error_message": "the description of requirement_content"}
            elif expected_completion_time == "":
                resp = {"success": "false", "error_message": "the description of expected_completion_time"}
            else:
                resp = {"success": "true", "error_message": ""}
            # resp = requests.request(
            #     url=input_body["endpoint"],
            #     method=input_body["method"],
            #     headers=input_body["headers"],
            #     params=input_body["params"],
            #     data=input_body["data"]
            # )
            return resp
        except Exception as e:
            return repr(e)
