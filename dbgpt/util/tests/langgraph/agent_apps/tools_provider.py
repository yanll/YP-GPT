from typing import Dict, Union, Any, Type, Callable, List

from langchain.tools import BaseTool
from langchain_core.utils.function_calling import convert_to_openai_tool
from pydantic import BaseModel

from dbgpt.util.tests.langgraph.tools.general_query_tool import GeneralQueryTool
from dbgpt.util.tests.langgraph.tools.requirement_tool import RequirementCollectTool


class ToolsProvider:
    general_tools: List[Union[Dict[str, Any], Type[BaseModel], Callable, BaseTool]] = []

    def __init__(self, *args, **kwargs):
        self.general_tools = [
            GeneralQueryTool(max_results=20),
            RequirementCollectTool()
        ]
        pass

    def converted_tools_info(self) -> Any:
        tools = []
        for tool in self.general_tools:
            tools.append(convert_to_openai_tool(tool))
        return tools
