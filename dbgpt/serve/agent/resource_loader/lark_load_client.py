import logging
from typing import Any, Dict, List, Optional, Tuple, Union

from dbgpt._private.config import Config
from dbgpt.agent.resource.resource_api import AgentResource, ResourceType
from dbgpt.agent.resource.resource_lark_api import ResourceLarkClient
from dbgpt.component import ComponentType
from dbgpt.util.executor_utils import ExecutorFactory, blocking_func_to_async
from dbgpt.util.larkutil import muti_table_add_record

CFG = Config()

logger = logging.getLogger(__name__)


class LarkLoadClient(ResourceLarkClient):
    def __init__(self):
        super().__init__()
        # The executor to submit blocking function
        self._executor = CFG.SYSTEM_APP.get_component(
            ComponentType.EXECUTOR_DEFAULT, ExecutorFactory
        ).create()

    def get_data_type(self, resource: AgentResource) -> str:
        # conn = CFG.local_db_manager.get_connector(resource.value)
        # return conn.db_type
        return "lark"

    # 执行AI前调用
    async def a_get_userinfo(self, db: str, question: Optional[str] = None) -> str:
        userinfo = {"username": "管理员", "email": "adm@adm.com"}
        return userinfo

    # 获取AI结果后调用
    async def a_query_to_df(self, db: str, sql: str):
        # conn = CFG.local_db_manager.get_connector(db)
        # return conn.run_to_df(sql)
        print("这里开始执行外部调用，Endpoint a_query_to_df！", sql)
        return "飞书接口调用完成，结果：{}"

    # 后置处理
    async def a_muti_table_add_record(self, app_id: str, table_id: str, record: dict) -> None:
        # conn = CFG.local_db_manager.get_connector(db)
        # return conn.query_ex(sql)
        print("这里开始执行外部调用，Endpoint a_query！", record)
        return muti_table_add_record(app_id=app_id, table_id=table_id, record=record)
