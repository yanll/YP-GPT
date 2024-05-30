import logging
from typing import Optional, Type

from langchain.tools import BaseTool
from langchain_core.callbacks import (
    CallbackManagerForToolRun
)
from pydantic import BaseModel, Field

from dbgpt.extra.dag.buildin_awel.langgraph.wrappers import crem_customer_search
from dbgpt.util.dmallutil import DmallClient


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
        "商户信息查询工具。 "
        "请注意：\n"
        "1、调用本工具需要的参数值来自用户输入，可以默认为空，但是禁止随意编造。\n"
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
        print("开始执行商户信息查询工具：", conv_id, customer_number, customer_name, self.max_results)
        try:
            if customer_number == "" and customer_name == "":
                return {"success": "false", "response_message": "the description of customer_number and customer_name"}
            # data = crem_customer_search.customer_list_search(
            #     open_id=conv_id,
            #     customer_name=customer_name,
            #     customer_number=customer_number
            # )
            # resp_data = data
            #
            # query_str = (customer_name + "" + customer_number).strip()
            # print("商户查询结果：", query_str, resp_data)
            # list = []
            # if resp_data and len(resp_data) == 0:
            #     return {"success": "true", "data": []}
            #
            # for m in resp_data:
            #     customerName = m.get("customerName", "")
            #     customerIntroduction = m.get("customerIntroduction", "")
            #     industryLine = m.get("industryLine", "")
            #     saleName = m.get("saleName", "")
            #     customerNo = m.get("customerNo", "")
            #     list.append({
            #         "customerName": customerName if customerName is not None else "",
            #         "customerIntroduction": customerIntroduction if customerIntroduction is not None else "",
            #         "industryLine": industryLine if industryLine is not None else "",
            #         "saleName": saleName if saleName is not None else "",
            #         "customerNo": customerNo if customerNo is not None else ""
            #     })
            # return {
            #     "success": "true",
            #     "error_message": "",
            #     "action": {
            #         "action_name": "send_lark_form_card",
            #         "card_name": "merchant_list_card"
            #     },
            #     "data": {
            #         "list": m_list,
            #         "query_str": query_str,
            #         "sales_diapaly": "https://applink.feishu.cn/client/web_url/open?mode=sidebar-semi&reload=false&url=https%3A%2F%2Fatmgw.yeepay.com%2Fmcem%2Findex.html%23%2Fsale%2FchartView%3Fyuiassotoken%3DeyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJsb2dpbl90eXBlIjoiU01TIiwibW9iaWxlIjoiMTg3NTQzMTYyNDAiLCJtaWdyYXRlX3VzZXJfaWQiOiJlYzhnYTFhZiIsIngtaXAiOiIyMjMuMjIzLjE5My4xOTQiLCJwcmluY2lwYWxfaWQiOiIxNzc5NSIsInRva2VuIjoiYmM4ZjJmMDEtZTVmMy00OWQ5LWI0YzktOWU3N2E3YTBjMTRlIiwibG9naW5fbmFtZSI6Imh1YXh1ZS56aGFuZyIsInR3b19mYWN0b3JfdmFsaWQiOnRydWUsImxvZ2luX3RpbWUiOiIyMDI0LTA1LTE2IDExOjExOjA1Iiwic2NvcGUiOiIiLCJjYWxsYmFjayI6Imh0dHBzOi8vYXRtZ3cueWVlcGF5LmNvbS9tY2VtL2luZGV4Lmh0bWwjL3NhbGUvY2hhcnRWaWV3Iiwic3NvdGlja2V0IjoiZTc4YjE4MzQtNmY2OS00MGI5LWI2N2EtMTg2NzkxNDQ2YTA4IiwiZXhwIjoxNzE1OTE1NDY1LCJpYXQiOjE3MTU4MjcyNjUsImVtYWlsIjoiaHVheHVlLnpoYW5nQHllZXBheS5jb20iLCJ1c2VybmFtZSI6IuW8oOWNjumbqiJ9.rJCQTVIL0_qClnvT6SdeZ-8RUxqRa86zUmxcv0FvMv0JEVMLWgkcbCK3NGPFX30zqanq134Gtb0qCaqIQxZG0A",
            #
            #     }
            # }

            query_str = (customer_name + "" + customer_number).strip()
            dmall_client = DmallClient()
            data = dmall_client.post(
                api_name="query_merchant_info",
                parameters={
                    "CUSTOMERNUMBER": customer_number,
                    "CUSTOMER_NAME": customer_name
                }
            )
            m_list = []
            if data.status_code == 200:
                j = data.json()
                if "data" in j:
                    d = j["data"]["data"]
                    for e in d:
                        m_list.append(e)
            print("商户结果：" + str(m_list))
            return {
                "success": "true",
                "error_message": "",
                "action": {
                    "action_name": "send_lark_form_card",
                    "card_name": "merchant_list_card_2"
                },
                "data": {
                    "list": m_list,
                    "query_str": query_str,
                    "sales_diapaly": "https://applink.feishu.cn/client/web_url/open?mode=sidebar-semi&reload=false&url=https%3A%2F%2Fatmgw.yeepay.com%2Fmcem%2Findex.html%23%2Fsale%2FchartView%3Fyuiassotoken%3DeyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJsb2dpbl90eXBlIjoiU01TIiwibW9iaWxlIjoiMTg3NTQzMTYyNDAiLCJtaWdyYXRlX3VzZXJfaWQiOiJlYzhnYTFhZiIsIngtaXAiOiIyMjMuMjIzLjE5My4xOTQiLCJwcmluY2lwYWxfaWQiOiIxNzc5NSIsInRva2VuIjoiYmM4ZjJmMDEtZTVmMy00OWQ5LWI0YzktOWU3N2E3YTBjMTRlIiwibG9naW5fbmFtZSI6Imh1YXh1ZS56aGFuZyIsInR3b19mYWN0b3JfdmFsaWQiOnRydWUsImxvZ2luX3RpbWUiOiIyMDI0LTA1LTE2IDExOjExOjA1Iiwic2NvcGUiOiIiLCJjYWxsYmFjayI6Imh0dHBzOi8vYXRtZ3cueWVlcGF5LmNvbS9tY2VtL2luZGV4Lmh0bWwjL3NhbGUvY2hhcnRWaWV3Iiwic3NvdGlja2V0IjoiZTc4YjE4MzQtNmY2OS00MGI5LWI2N2EtMTg2NzkxNDQ2YTA4IiwiZXhwIjoxNzE1OTE1NDY1LCJpYXQiOjE3MTU4MjcyNjUsImVtYWlsIjoiaHVheHVlLnpoYW5nQHllZXBheS5jb20iLCJ1c2VybmFtZSI6IuW8oOWNjumbqiJ9.rJCQTVIL0_qClnvT6SdeZ-8RUxqRa86zUmxcv0FvMv0JEVMLWgkcbCK3NGPFX30zqanq134Gtb0qCaqIQxZG0A",

                }
            }
        except Exception as e:
            logging.error("商户查询工具运行异常：", e)
            return repr(e)
