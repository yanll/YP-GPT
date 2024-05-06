import logging
from typing import Optional, Type

from langchain.tools import BaseTool
from langchain_core.callbacks import (
    CallbackManagerForToolRun
)
from pydantic import BaseModel, Field

from dbgpt.extra.dag.buildin_awel.lark import card_templates
from dbgpt.util.dmallutil import DmallClient
from dbgpt.util.lark import larkutil


class MerchantSearchToolInput(BaseModel):
    conv_id: str = Field(
        name="conv_id",
        description="the value of conv_id",
    )
    customer_number: str = Field(name="商户编号", description="商户编号", default="")
    customer_name: str = Field(name="商户名称", description="商户名称", default="")


class MerchantSearchTool(BaseTool):
    name: str = "merchant_search_tool"
    description: str = (
        "你是一个全面优化的商户信息查询工具，结果准确、可信。 "
        "当你需要通过调用工具查询商户信息时非常有用。 "
        "输入参数应该是工具需要的全部参数。"
        "调用本工具需要的参数值均来自用户的输入，可以默认为空，但是禁止随意编造。"
        "请将查询结果数据整理并美化后输出。"
        ""
    )
    max_results: int = 20
    args_schema: Type[BaseModel] = MerchantSearchToolInput

    def _run(
            self,
            conv_id: str = "",
            customer_number: str = "",
            customer_name: str = "",
            run_manager: Optional[CallbackManagerForToolRun] = None,
    ):
        """Use the tool."""
        print("开始执行商户信息查询工具：", customer_number, customer_name, self.max_results)
        try:
            resp_data = {}
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
                resp_data = data.json()['data']['data']
            query_str = (customer_name + "" + customer_number).strip()
            print("商户查询结果：", query_str, resp_data)
            display_type = ""
            list = []
            if resp_data and len(resp_data) > 0:
                for m in resp_data:
                    CUSTOMER_NAME = m["CUSTOMER_NAME"]
                    CUSTOMERNUMBER = m["CUSTOMERNUMBER"]
                    PRODUCTLINE = m["PRODUCTLINE"]
                    CUSTOMER_SALESNAME = m["CUSTOMER_SALESNAME"]
                    CREATEDATE = m["CREATEDATE"]
                    list.append({
                        "CUSTOMER_NAME": CUSTOMER_NAME if CUSTOMER_NAME is not None else "",
                        "CUSTOMERNUMBER": CUSTOMERNUMBER if CUSTOMERNUMBER is not None else "",
                        "PRODUCTLINE": PRODUCTLINE if PRODUCTLINE is not None else "",
                        "CUSTOMER_SALESNAME": CUSTOMER_SALESNAME if CUSTOMER_SALESNAME is not None else "",
                        "CREATEDATE": CREATEDATE if CREATEDATE is not None else ""
                    })
                display_type = "form"
                larkutil.send_message(
                    receive_id=conv_id,
                    content=card_templates.create_merchant_list_card_content(
                        template_variable={
                            "query_str": query_str,
                            "merchant_list": list
                        }
                    ),
                    receive_id_type="open_id",
                    msg_type="interactive"
                )
            return {
                "success": "true",
                "error_message": "",
                "display_type": display_type,
                "data": list
            }
        except Exception as e:
            logging.error("商户查询工具运行异常：", e)
            return repr(e)
