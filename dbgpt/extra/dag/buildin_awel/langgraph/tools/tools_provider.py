from typing import Dict, Union, Any, Type, Callable, List

from langchain.tools import BaseTool
from langchain_core.utils.function_calling import convert_to_openai_tool
from pydantic import BaseModel

from dbgpt.extra.dag.buildin_awel.langgraph.tools.crm_bus_customer_add_tool import CrmBusCustomerCollectAddTool
from dbgpt.extra.dag.buildin_awel.langgraph.tools.crm_bus_customer_query_tool import CrmBusCustomerCollectQueryTool
from dbgpt.extra.dag.buildin_awel.langgraph.tools.customer_visit_record_tool import CustomerVisitRecordCollectTool
from dbgpt.extra.dag.buildin_awel.langgraph.tools.daily_report_search_tool import DailyReportSearchTool
from dbgpt.extra.dag.buildin_awel.langgraph.tools.daily_report_tool import DailyReportCollectTool
from dbgpt.extra.dag.buildin_awel.langgraph.tools.feedback_tool import FeedbackCollectTool
from dbgpt.extra.dag.buildin_awel.langgraph.tools.knowledge_tool import KnowledgeTool
from dbgpt.extra.dag.buildin_awel.langgraph.tools.merchant_search_tool import MerchantSearchTool
from dbgpt.extra.dag.buildin_awel.langgraph.tools.requirement_search_tool import RequirementSearchTool
from dbgpt.extra.dag.buildin_awel.langgraph.tools.requirement_tool import RequirementCollectTool
from dbgpt.extra.dag.buildin_awel.langgraph.tools.weekly_report_tool import WeeklyReportCollectTool


class ToolsProvider:
    general_tools: List[Union[Dict[str, Any], Type[BaseModel], Callable, BaseTool]] = []

    def __init__(self, *args, **kwargs):
        self.general_tools = [
            MerchantSearchTool(max_results=10),
            DailyReportCollectTool(),
            DailyReportSearchTool(),
            WeeklyReportCollectTool(),
            CustomerVisitRecordCollectTool(),
            RequirementSearchTool(),
            RequirementCollectTool(),
            CrmBusCustomerCollectAddTool(),
            CrmBusCustomerCollectQueryTool(),
            FeedbackCollectTool(),
            KnowledgeTool()
        ]
        pass

    def converted_tools_info(self) -> Any:
        tools = []
        for tool in self.general_tools:
            tools.append(convert_to_openai_tool(tool))
        return tools
