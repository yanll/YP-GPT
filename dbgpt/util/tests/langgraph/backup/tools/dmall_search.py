"""数据商店接口调用工具.

In order to set this up, follow instructions at:
"""
from typing import Dict, List, Optional

from langchain_core.pydantic_v1 import BaseModel, Extra, root_validator

from dbgpt.util.dmallutil import DmallClient


class DmallSearchAPIWrapper(BaseModel):
    """数据商店接口包装器"""

    endpoint: str = "https://dmall."

    class Config:
        """Configuration for this pydantic object."""
        extra = Extra.forbid

    @root_validator(pre=True)
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that endpoint exists in environment."""
        values["endpoint"] = ""
        return values

    def raw_results(
            self,
            api_name: str,
            api_parameters: str,
            api_version: Optional[str] = "V1.0"
    ) -> Dict:
        params = {
            "api_name": api_name,
            "api_parameters": api_parameters,
            "api_version": api_version
        }

        dmall_client = DmallClient()
        data = dmall_client.post(
            api_name=params["api_name"],
            parameters={
                "CUSTOMERNUMBER2": params["api_parameters"]
            },
            api_version=params["api_version"]
        )
        return data.json()

    def results(
            self,
            api_name: str,
            api_parameters: str,
            api_version: str
    ) -> List[Dict]:
        """Run call through Dmall Search and return metadata.

        Args:
            api_name: 数据商店接口名称
            api_parameters: 数据商店接口参数对象
            api_version: 数据商店接口版本
        Returns:
            follow_up_questions: A list of follow up questions.
            response_time: The response time of the query.
            results: A list of dictionaries containing the results:

        """
        raw_search_results = self.raw_results(
            api_name=api_name,
            api_parameters=api_parameters,
            api_version=api_version
        )
        return raw_search_results["data"]
