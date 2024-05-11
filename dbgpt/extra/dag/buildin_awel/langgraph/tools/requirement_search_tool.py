
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
    work_status: str = Field(
        name="需求状态",
        description="需求状态",
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
            work_status: str = "",
            #requirement_create_name: str = "",
            run_manager: Optional[CallbackManagerForToolRun] = None,
    ):
        """Use the tool."""
        global industry_line_mapping
        """参数别动，我还用，-_-"""
        #print("开始执行需求信息查询工具：", conv_id, industry_line,emergency_level,requirement_create_name, self.max_results)
        print("开始执行需求信息查询工具：", conv_id, industry_line,emergency_level,work_status, self.max_results)
        try:
            resp_data = {}
            if conv_id == "":
                return {"success": "false", "response_message": "the description of conv_id"}

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
            work_status_mapping = {
                "受理中": "sub_stage_1659349204962",
            }
            business_value = industry_line_mapping.get(industry_line, "")
            priority_value = emergency_level_mapping.get(emergency_level, "")
            work_status_value = work_status_mapping.get(work_status, "")


            requirement_search_analysis = lark_project_requirement_search.create_requirement_search_for_lark_project(
                union_id=conv_id,
                project_key="ypgptapi",
                requirement_create_name="",
                business_value=business_value,
                priority_value=priority_value,
                work_status_value=work_status_value
            )
            print("完整返回结果", requirement_search_analysis)
            #extracted_info = requirement_search_analysis[0]
            extracted_info = requirement_search_analysis

            print("需求查询返回结果", extracted_info)


            resp_data = {}
            resp_data = extracted_info

            # 获取行业线名称
            industry_line = industry_line
            # 若行业线为空，则显示"行业线：全部行业线"
            if not industry_line:
                industry_line = "全部行业线"
            # 若优先级为空，则显示"优先级：所有级别"
            if not emergency_level:
                emergency_level = "所有级别"
            if not work_status:
                work_status = "所有状态"
            # 构造查询字符串
            query_str = (
                    "行业线：" + industry_line + "\n" +
                    "紧急程度：" + emergency_level + "\n"+
                    "需求状态：" + work_status + "\n"
            ).strip()

            print("需求池详情查询结果：", query_str, resp_data)
            list = []
            if resp_data and len(resp_data) == 0:
                return {"success": "true", "data": []}

            for m in resp_data:
                name = m.get("name", "")
                exp_time = m.get("exp_time", "")
                priority_label = m.get("priority_label", "")
                business_id = m.get("business_id", "")
                start_time = m.get("start_time", "")
                owner = m.get("owner", "")
                state_key = m.get("state_key", "")
                # 将 business_id 转换为行业线名称
                industry_line_mapping_fan = {
                    "662db530cde8ed174622a08d": "航旅行业线",
                    "662db56afe2c0b51b33668eb": "大零售行业线",
                    "662db596fe2c0b51b33668ec": "线上线下一体化",
                    "662db5b688aa18a943e64644": "老板管账",
                    "662db5c3a55775e2c9c83bf9": "金融行业线"
                }
                work_status_mapping_fan = {
                    "sub_stage_1659349204962": "受理中"
                }
                if business_id in industry_line_mapping_fan:
                    business_id = industry_line_mapping_fan[business_id]
                    print("转换以后的结果", business_id)
                if state_key in work_status_mapping_fan:
                    state_key = work_status_mapping_fan[state_key]
                    print("转换以后的结果", state_key)

                list.append({
                    "owner": owner if owner is not None else "",
                    "start_time": start_time if start_time is not None else "",
                    "business_id": business_id if business_id is not None else "",
                    "priority_label": priority_label if priority_label is not None else "",
                    "exp_time": exp_time if exp_time is not None else "",
                    "name": name if name is not None else "",
                    "state_key": state_key if state_key is not None else ""
                })

            return {
                "success": "true",
                "error_message": "",
                "action": {
                    "action_name": "send_lark_form_card",
                    "card_name": "requirement_search_list"
                },
                "data": {
                    "list": list,
                    "query_str": query_str
                }
            }
        except Exception as e:
            logging.error("商户查询工具运行异常：", e)
            return repr(e)

