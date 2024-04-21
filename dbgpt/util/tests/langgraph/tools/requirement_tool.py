from typing import Optional, Type

from langchain.tools import BaseTool
from langchain_core.callbacks import (
    CallbackManagerForToolRun,
)
from pydantic import BaseModel, Field

from dbgpt.util import larkutil


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
    expected_completion_time: str = Field(
        name="期望完成时间",
        description="期望完成时间",
        default=""
    )
    emergency_level: str = Field(
        name="紧急程度",
        description="紧急程度",
        default=""
    )


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
            conv_id: str = "",
            requirement_content: str = "",
            expected_completion_time: str = "",
            emergency_level: str = "",
            run_manager: Optional[CallbackManagerForToolRun] = None,
    ):
        """Use the tool."""
        print("开始运行需求收集工具：", conv_id, requirement_content, emergency_level, expected_completion_time)
        try:
            if requirement_content == "":
                resp = {"success": "false", "response_message": "the description of requirement_content"}
            elif expected_completion_time == "":
                resp = {"success": "false", "response_message": "the description of expected_completion_time"}
            elif emergency_level == "":
                resp = {"success": "false", "response_message": "the description of emergency_level"}
            else:
                resp = do_collect(
                    requirement_content=requirement_content,
                    expected_completion_time=expected_completion_time,
                    emergency_level=emergency_level)
            return resp
        except Exception as e:
            return repr(e)


def do_collect(
        requirement_content: str = "",
        expected_completion_time: str = "",
        emergency_level: str = ""
):
    # print("开始执行需求收集：", requirement_content, emergency_level, expected_completion_time)
    # resp = requests.request(
    #     url=input_body["endpoint"],
    #     method=input_body["method"],
    #     headers=input_body["headers"],
    #     params=input_body["params"],
    #     data=input_body["data"]
    # )
    if False:
        larkutil.send_message("liangliang.yan@yeepay.com", {"text": "hello!"})
    return {
        "success": "true", "error_message": "", "data": {
            "requirement_content": requirement_content,
            "expected_completion_time": expected_completion_time,
            "emergency_level": emergency_level
        }
    }
