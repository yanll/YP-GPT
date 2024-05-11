
import logging
from typing import Optional, Type

from langchain.tools import BaseTool
from langchain_core.callbacks import (
    CallbackManagerForToolRun,
)
from pydantic import BaseModel, Field

from dbgpt.extra.dag.buildin_awel.langgraph.wrappers import lark_project_requirement_search
from dbgpt.extra.dag.buildin_awel.lark import card_templates
from dbgpt.util.lark import lark_message_util, lark_card_util


class RequirementSearchToolInput(BaseModel):
    conv_id: str = Field(
        name="conv_id",
        description="the value of conv_id",
    )
    industry_line: str = Field(
        name="行业线",
        description="行业线",
        default=""
    )
    emergency_level: str = Field(
        name="紧急程度",
        description="紧急程度",
        default=""
    )
    # requirement_create_name: str = Field(
    #     name="需求创建者名称", description="需求创建者名称", default="")



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
            #requirement_create_name: str = "",
            run_manager: Optional[CallbackManagerForToolRun] = None,
    ):
        """Use the tool."""
        global industry_line_mapping
        """参数别动，我还用，-_-"""
        #print("开始执行需求信息查询工具：", conv_id, industry_line,emergency_level,requirement_create_name, self.max_results)
        print("开始执行需求信息查询工具：", conv_id, industry_line,emergency_level, self.max_results)
        lark_message_id = ""
        try:
            resp_data = {}
            if conv_id == "":
                resp = {"success": "false", "response_message": "the description of conv_id"}
            else:
                industry_line_mapping = {
                    "航旅行业线": "662db530cde8ed174622a08d",
                    "大零售行业线": "662db56afe2c0b51b33668eb",
                    "线上线下一体化": "662db596fe2c0b51b33668ec",
                    "老板管账": "662db5b688aa18a943e64644",
                    "金融行业线": "662db5c3a55775e2c9c83bf9"
                }
                emergency_level_mapping = {
                    "非常紧急": "0",
                    "紧急": "1",
                    "高": "2",
                    "中": "99",
                    "低": "1sdyyo6lh"
                }
                business_value = industry_line_mapping.get(industry_line, "")
                priority_value = emergency_level_mapping.get(emergency_level, "")

                requirement_search_analysis = lark_project_requirement_search.create_requirement_search_for_lark_project(
                    union_id=conv_id,
                    project_key="ypgptapi",
                    requirement_create_name="",
                    business_value=business_value,
                    priority_value=priority_value
                )
                print("完整返回结果", requirement_search_analysis)
                #extracted_info = requirement_search_analysis[0]
                extracted_info = requirement_search_analysis

                print("需求查询返回结果", extracted_info)


                resp_data = {}
                resp_data = extracted_info

            query_str = (
                    "行业线：" + industry_line + "\n"
                    "紧急程度:" + emergency_level + "\n"
                    #"需求创建人:" + requirement_create_name
            ).strip()
            print("需求池详情查询结果：", query_str, resp_data)
            display_type = ""
            list = []
            if resp_data and len(resp_data) > 0:
                for m in resp_data:
                    name = m.get("name", "")
                    exp_time = m.get("exp_time", "")
                    priority_label = m.get("priority_label", "")
                    business_id = m.get("business_id", "")
                    start_time = m.get("start_time", "")
                    owner = m.get("owner", "")
                    # 将 business_id 转换为行业线名称
                    industry_line_mapping_fan = {
                        "662db530cde8ed174622a08d": "航旅行业线",
                        "662db56afe2c0b51b33668eb": "大零售行业线",
                        "662db596fe2c0b51b33668ec": "线上线下一体化",
                        "662db5b688aa18a943e64644": "老板管账",
                        "662db5c3a55775e2c9c83bf9": "金融行业线"
                    }
                    if business_id in industry_line_mapping_fan:
                        business_id = industry_line_mapping_fan[business_id]
                        print("转换以后的结果",business_id)

                    list.append({
                        "owner": owner if owner is not None else "",
                        "start_time": start_time if start_time is not None else "",
                        "business_id": business_id if business_id is not None else "",
                        "priority_label": priority_label if priority_label is not None else "",
                        "exp_time": exp_time if exp_time is not None else "",
                        "name": name if name is not None else ""
                    })
                display_type = "form"
                lark_message_util.send_message(
                    receive_id=conv_id,
                    content=card_templates.requirement_search_list_card_content(
                        template_variable={
                            "query_str": query_str,
                            "requirement_search_list": list
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
            logging.error("需求查询工具运行异常：", e)
            return repr(e)

#
#
#
#


#
#
#
#
#
#
#
#
#
#
#
#
#


#
#
# class RequirementSearchToolInput(BaseModel):
#     conv_id: str = Field(
#         name="conv_id",
#         description="the value of conv_id",
#     )
#     industry_line: str = Field(
#         name="行业线",
#         description="行业线，" +
#                     lark_card_util.card_options_to_input_field_description(
#                         lark_card_util.card_options_for_requirement_industry_line()
#                     ),
#         default=""
#     )
#     emergency_level: str = Field(
#         name="紧急程度",
#         description="紧急程度，" +
#                     lark_card_util.card_options_to_input_field_description(
#                         lark_card_util.card_options_for_requirement_emergency_level()
#                     ),
#         default=""
#     )
#     requirement_create_name: str = Field(
#         name="需求创建者名称", description="需求创建者名称", default="")
#
#
# class RequirementSearchTool(BaseTool):
#     name: str = "requirement_search_tool"
#     description: str = (
#         "你是一个需求信息查询工具，用于需求查询，结果准确、可信。 "
#         "当你需要通过调用工具查询需求信息时非常有用。 "
#         "输入参数应该是工具需要的全部参数。"
#         "调用本工具需要的参数值均来自用户的输入，可以默认为空，但是禁止随意编造。"
#         "请将查询结果数据整理并美化后输出。"
#
#     )
#     max_results: int = 20
#     args_schema: Type[BaseModel] = RequirementSearchToolInput
#
#     def _run(
#             self,
#             conv_id: str = "",
#             industry_line: str = "",
#             emergency_level: str = "",
#             requirement_create_name: str = "",
#             run_manager: Optional[CallbackManagerForToolRun] = None,
#     ):
#         """Use the tool."""
#         print("开始执行需求信息查询工具：", conv_id, industry_line,emergency_level,requirement_create_name, self.max_results)
#         try:
#             if industry_line == "":
#                 resp = {"success": "false", "response_message": "the description of industry_line"}
#             elif emergency_level == "":
#                 resp = {"success": "false", "response_message": "the description of emergency_level"}
#             elif requirement_create_name == "":
#                 resp = {"success": "false", "response_message": "the description of requirement_create_name"}
#
#             else:
#                 resp = do_collect(
#                     conv_id=conv_id,
#                     industry_line=industry_line,
#                     emergency_level=emergency_level,
#                     requirement_create_name=requirement_create_name
#                 )
#             return resp
#         except Exception as e:
#             logging.error("工具运行异常：", e)
#             return repr(e)
#
# def do_collect(
#         conv_id: str = "",
#         industry_line: str = "",
#         emergency_level: str = "",
#         requirement_create_name: str = ""
#     ):
#     print("发送飞书需求提报卡片：", conv_id)
#     try:
#         """
#
#         """
#
#         lark_message_util.send_message(
#             receive_id=conv_id,
#             content=card_templates.requirement_search_card_content(
#                 template_variable={
#                     "card_metadata": {
#                         "card_name": "requirement_search",
#                         "description": "需求查询表单"
#                     },
#                     "industry_line": lark_card_util.get_action_index_by_text_from_options(
#                         industry_line,
#                         lark_card_util.card_options_for_requirement_industry_line()
#                     ),
#                     "industry_line_options": lark_card_util.card_options_for_requirement_industry_line(),
#                     "emergency_level": lark_card_util.get_action_index_by_text_from_options(
#                         emergency_level,
#                         lark_card_util.card_options_for_requirement_emergency_level()
#                     ),
#                     "emergency_level_options": lark_card_util.card_options_for_requirement_emergency_level(),
#                     "requirement_create_name": requirement_create_name,
#
#                 }
#             ),
#             receive_id_type="open_id",
#             msg_type="interactive"
#         )
#     except Exception as e:
#         logging.error("飞书需求提报卡片发送失败：", e)
#
#     return {
#         "success": "true",
#         "error_message": "",
#         "display_type": "form",
#         "data": {
#             "conv_id": conv_id,
#             "industry_line": industry_line,
#             "requirement_create_name": requirement_create_name,
#             "emergency_level": emergency_level
#         }
#     }