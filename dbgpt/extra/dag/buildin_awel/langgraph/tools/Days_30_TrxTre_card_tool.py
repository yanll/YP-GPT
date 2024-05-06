# 导入必要的模块
import requests
from dbgpt.extra.dag.buildin_awel.langgraph.wrappers.crem_30DaysTrxTre_card import get_crem_30DaysTrxTre_card  # 确保此模块路径正确


import logging
from typing import Optional, Type
from typing import List

from langchain.tools import BaseTool
from langchain_core.callbacks import (
    CallbackManagerForToolRun,
)
from pydantic import BaseModel, Field

import logging
from typing import Optional, Type
from typing import List

from langchain.tools import BaseTool
from langchain_core.callbacks import (
    CallbackManagerForToolRun,
)
from pydantic import BaseModel, Field

from dbgpt.extra.dag.buildin_awel.lark import card_templates
from dbgpt.util.lark import larkutil


class Days30TrxTrecard(BaseModel):
    """

    """
    conv_id: str = Field(
        name="conv_id",
        description="the value of conv_id",
    )
    customer_id: str = Field(
        name="商编id",
        description="商编id",
        default=""
    )



class Days30TrxTrecardTool(BaseTool):
    name: str = "daily_report_collect_tool"
    description: str = (
        "这是一个日报填写工具，帮助用户每天填写工作日报、每日工作总结。"
        "当需要填写日报时非常有用。 "
        "能够尽可能全的收集日报信息。"
        "调用本工具需要的参数值均来自用户的输入，可以默认为空，但是禁止随意编造。"
        ""
    )
    args_schema: Type[BaseModel] = Days30TrxTrecard

    def _run(
            self,
            conv_id: str = "",
            customer_id: str = "",

            run_manager: Optional[CallbackManagerForToolRun] = None,
    ):
        """Use the tool."""
        print("开始运行日报填写工具：", conv_id, customer_id)
        try:
            if conv_id == "":
                resp = {"success": "false", "response_message": "the description of daily_report_content"}
            elif customer_id == "":
                resp = {"success": "false", "response_message": "the description of create_date"}
            else:
                resp = do_collect(
                    conv_id=conv_id,
                    customer_id=customer_id,
                )
            return resp
        except Exception as e:
            logging.error("工具运行异常：", e)
            return repr(e)


def do_collect(
        conv_id: str = "",
        customer_id: str = "",

):

    try:
        """
        我要填写日报：
        日报内容：今天完成了一次客户回访，进展正常。
        填写日期：2024-04-22
        明日计划：继续跟进
        """
        print("发送飞书日报卡片：", conv_id)
        larkutil.send_message(
            receive_id=conv_id,
            content=card_templates.create_daily_report_card_content(
                template_variable={
                    "card_metadata": {
                        "card_name": "daily_report_collect",
                        "description": "日报收集表单"
                    },
                    "customer_id": customer_id,
                }
            ),
            receive_id_type="open_id",
            msg_type="interactive"
        )
    except Exception as e:
        logging.error("飞书日报卡片发送失败：", e)

    # 创建并返回结果字典
    return {
        "success": "true",
        "error_message": "",
        "display_type": "form",
        "data": {
            "conv_id": conv_id,
            "customer_id": customer_id,

        }
    }

# 调用第一个代码文件中的函数来获取数据
customer_id = "KA2021-A11220743"
customer_info = get_crem_30DaysTrxTre_card(customer_id)

# 提取所需字段并转换为生成图表所需的格式
if 'data' in customer_info and 'data' in customer_info['data']:
    formatted_data = []
    for item in customer_info['data']['data']:
        formatted_item = {
            "time": item["jiaoyiriqi"],  # 将交易日期作为 time
            "value": item["maoli"]  # 将毛利作为 value
        }
        formatted_data.append(formatted_item)
else:
    formatted_data = []  # 如果没有数据或者请求失败，设置为空列表


# 提取所需字段并转换为生成图表所需的格式
if 'data' in customer_info and 'data' in customer_info['data']:
    formatted_data_jiaoyijine = []
    for item in customer_info['data']['data']:
        formatted_item = {
            "time": item["jiaoyiriqi"],  # 将交易日期作为 time
            "value": item["jiaoyijine"]  # 将交易金额作为 value
        }
        formatted_data_jiaoyijine.append(formatted_item)
else:
    formatted_data_jiaoyijine = []  # 如果没有数据或者请求失败，设置为空列表
# 图表配置
var = {
    "config": {},
    "i18n_elements": {
        "zh_cn": [
            {
                "tag": "chart",
                "chart_spec": {
                    "type": "area",
                    "title": {"text": "近30天毛利"},
                    "data": {"values": formatted_data},  # 更新数据部分
                    "xField": "time",
                    "yField": "value",
                },
            }
        ]
    },
    "i18n_header": {}
}


var2 = {
    "config": {},
    "i18n_elements": {
        "zh_cn": [
            {
                "tag": "chart",
                "chart_spec": {
                    "type": "area",
                    "title": {"text": "近30天交易金额"},
                    "data": {"values": formatted_data_jiaoyijine},  # 更新数据部分
                    "xField": "time",
                    "yField": "value",
                },
            }
        ]
    },
    "i18n_header": {}
}

# 打印更新后的图表配置，可以根据实际需求使用这个配置生成图表
print(var)
