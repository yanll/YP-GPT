"""数据商店查询数据工具"""

from typing import Dict, List, Optional, Type, Union

from langchain.pydantic_v1 import Field
from langchain.tools import BaseTool
from langchain_core.callbacks import CallbackManagerForToolRun
from pydantic import BaseModel

from .biz_exception import BizException
from .dmall_search import DmallSearchAPIWrapper


class DmallInput(BaseModel):
    """数据商店接口入参"""
    # api_name: str = Field(description="数据商店接口名称", include=["query_merchant_info", "meeting_rooms"])
    api_name: str = Field(
        title="接口名称",
        description="数据商店接口名称,must be in ['get_meeting_rooms','query_merchant_info']"
    )
    api_parameters: str = Field(
        title="接口参数", description="数据商店接口参数,must be from human"
    )
    api_version: str = Field(
        title="数据商店接口版本", description="", default=""
    )


class DmallSearchResults(BaseTool):
    """Tool that queries the Dmall Search API and gets back json."""
    name: str = "dmall_search_results_json"
    description: str = (
        "你是一个全面优化的数据商店接口调用工具，调用结果准确、可信。"
        "当你需要查询商户信息时非常有用。"
        "输入应该是数据商店接口调用需要的全部参数。"
        ""
    )
    api_wrapper: DmallSearchAPIWrapper = Field(default_factory=DmallSearchAPIWrapper)
    max_results: int = 20
    args_schema: Type[BaseModel] = DmallInput

    def _run(
            self,
            api_name: str,
            api_parameters: str,
            api_version: str = "V1.0",
            run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Union[List[Dict], str]:
        """Use the tool."""
        try:
            if True:
                raise BaseException("请输入编号!")
            return []
            # return self.api_wrapper.results(
            #     api_name=api_name,
            #     api_parameters=api_parameters,
            #     api_version=api_version
            # )
        except Exception as e:
            return repr(e)


class DmallAnswer(BaseTool):
    """Tool that queries the Dmall Search API and gets back an answer."""
    name: str = "dmall_answer"
    description: str = (
        "A search engine optimized for comprehensive, accurate, and trusted results. "
        "Useful for when you need to answer questions about current events. "
        "输入应该是数据商店接口调用需要的全部参数。"
        "This returns only the answer - not the original source data."
    )
    api_wrapper: DmallSearchAPIWrapper = Field(default_factory=DmallSearchAPIWrapper)
    args_schema: Type[BaseModel] = DmallInput

    def _run(
            self,
            api_name: str,
            api_parameters: str,
            api_version: str,
            run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Union[List[Dict], str]:
        """Use the tool."""
        try:
            return self.api_wrapper.raw_results(
                api_name=api_name,
                api_parameters=api_parameters,
                api_version=api_version
            )["answer"]
        except Exception as e:
            return repr(e)
