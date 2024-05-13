"""通用查询工具"""
import json
from typing import Dict, List, Optional, Type, Union, Any

from langchain_core.callbacks import (
    CallbackManagerForToolRun,
)
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.tools import BaseTool

import requests

from dbgpt.util import consts


class GeneralQueryToolInput(BaseModel):
    """通用查询工具的输入参数"""

    input_body: Dict = Field(description="输入参数对象", default={})


class GeneralQueryResults(BaseTool):
    """调用API并返回JSON数据的通用查询工具"""

    name: str = "general_query_results_json"
    description: str = (
        "你是一个全面优化的API调用工具，调用结果准确、可信。 "
        "当你需要通过调用API查询数据时非常有用。 "
        "输入参数应该是API需要的全部参数。"
        ""
    )
    max_results: int = 20
    args_schema: Type[BaseModel] = GeneralQueryToolInput

    def _run(
            self,
            input_body: Optional[Dict],
            run_manager: Optional[CallbackManagerForToolRun] = None,
    ):
        """Use the tool."""
        try:
            resp = requests.request(
                url=input_body["endpoint"],
                method=input_body["method"],
                headers=input_body["headers"],
                params=input_body["params"],
                data=input_body["data"],
                timeout=consts.request_time_out
            )
            return resp
        except Exception as e:
            return repr(e)


class GeneralQueryAnswer(BaseTool):
    """调用API并返回结果的通用查询工具"""

    name: str = "general_query_answer"
    description: str = (
        "A api caller optimized for comprehensive, accurate, and trusted results. "
        "Useful for when you need to answer questions about current events. "
        "This returns only the answer - not the original source data."
    )
    args_schema: Type[BaseModel] = GeneralQueryToolInput

    def _run(
            self,
            input_body: Dict,
            run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Union[Any, str]:
        """Use the tool."""
        try:
            resp = requests.request(
                url=input_body["endpoint"],
                method=input_body["method"],
                headers=input_body["headers"],
                params=input_body["params"],
                data=input_body["data"],
                timeout=consts.request_time_out
            )
            return [resp, "answer"]
        except Exception as e:
            return repr(e)
