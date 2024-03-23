import logging
from contextlib import contextmanager
from typing import Any, Dict, List, Optional, Tuple, Union

from dbgpt.agent.resource.resource_api import AgentResource

from .resource_api import ResourceClient, ResourceType

logger = logging.getLogger(__name__)


class ResourceLarkClient(ResourceClient):
    @property
    def type(self):
        return ResourceType.LarkApi

    def get_data_type(self, resource: AgentResource) -> str:
        return super().get_data_type(resource)

    async def get_data_introduce(
            self, resource: AgentResource, question: Optional[str] = None
    ) -> str:
        return await self.a_get_userinfo(resource.value, question)

    async def a_get_userinfo(self, db: str, question: Optional[str] = None) -> str:
        raise NotImplementedError("The run method should be implemented in a subclass.")

    async def a_query_to_df(self, dbe: str, sql: str):
        raise NotImplementedError("The run method should be implemented in a subclass.")

    async def a_query(self, db: str, sql: str):
        raise NotImplementedError("The run method should be implemented in a subclass.")

    async def a_run_sql(self, db: str, sql: str):
        raise NotImplementedError("The run method should be implemented in a subclass.")


class MockResourceLarkClient(ResourceLarkClient):
    pass
