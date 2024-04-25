import logging
from typing import Optional, Type

from langchain.tools import BaseTool
from langchain_core.callbacks import (
    CallbackManagerForToolRun
)
from pydantic import BaseModel, Field

from dbgpt.util.dmallutil import DmallClient


class MerchantSearchToolInput(BaseModel):
    customer_number: str = Field(name="客户/商户编号", description="客户/商户编号", default="")
    customer_name: str = Field(name="客户/商户名称", description="客户/商户名称", default="")


class MerchantSearchTool(BaseTool):
    name: str = "merchant_search_tool"
    description: str = (
        "你是一个全面优化的商户信息和客户信息查询工具，结果准确、可信。 "
        "当你需要通过调用工具查询商户或客户信息时非常有用。 "
        "输入参数应该是工具需要的全部参数。"
        "调用本工具需要的参数值均来自用户的输入，可以默认为空，但是禁止随意编造。"
        "请将查询结果数据整理并美化后输出。"
        ""
    )
    max_results: int = 20
    args_schema: Type[BaseModel] = MerchantSearchToolInput

    def _run(
            self,
            customer_number: str = "",
            customer_name: str = "",
            run_manager: Optional[CallbackManagerForToolRun] = None,
    ):
        """Use the tool."""
        print("开始执行商户信息查询工具：", customer_number, customer_name, self.max_results)
        try:
            if customer_number == "" and customer_name == "":
                resp = {"success": "false", "response_message": "the description of customer_number and customer_name"}
            else:
                dmall_client = DmallClient()
                data = dmall_client.post(
                    api_name="query_merchant_info",
                    parameters={
                        "CUSTOMERNUMBER": customer_number,
                        "CUSTOMER_NAME": customer_name
                    }
                )
                resp = data.json()['data']['data']
            return resp
        except Exception as e:
            logging.error("商户查询工具运行异常：", e)
            return repr(e)
