from typing import Dict, Optional, Type, Union, Any

import requests
from langchain.tools import BaseTool
from langchain_core.callbacks import (
    CallbackManagerForToolRun,
)
from pydantic import BaseModel, Field


class GeneralQueryToolInput(BaseModel):
    api_name: str = Field(name="接口名称", description="接口名称，如果用户没有输入，提醒用户输入，不要生成此项")
    api_params: str = Field(name="接口参数对象", description="接口参数对象，JSON格式的对象，例如：{\"id\":\"10000\"}")
    api_version: str = Field(name="接口版本", description="接口版本", default="")


class GeneralQueryTool(BaseTool):
    name: str = "general_query_tool"
    description: str = (
        "你是一个全面优化的接口调用工具，结果准确、可信。 "
        "当你需要通过调用工具查询数据时非常有用。 "
        "输入参数应该是工具需要的全部参数。"
        ""
    )
    max_results: int = 20
    args_schema: Type[BaseModel] = GeneralQueryToolInput

    def _run(
            self,
            api_name: str,
            api_params: Dict = {},
            api_version: str = "V0.0.1",
            run_manager: Optional[CallbackManagerForToolRun] = None,
    ):
        """Use the tool."""
        print("开始执行通用查询工具")
        try:
            resp = {

            }
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
