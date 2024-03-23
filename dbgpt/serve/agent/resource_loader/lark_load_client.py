import logging
from typing import Optional

from dbgpt._private.config import Config
from dbgpt.agent.resource.resource_api import AgentResource
from dbgpt.agent.resource.resource_lark_api import ResourceLarkClient
from dbgpt.component import ComponentType
from dbgpt.util.executor_utils import ExecutorFactory
from dbgpt.util.larkutil import muti_table_add_record, send_message

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
    async def a_muti_table_add_record(self, app_id: str, table_id: str, record: dict) -> None:
        # conn = CFG.local_db_manager.get_connector(db)
        # return conn.query_ex(sql)
        print("这里开始执行外部调用，Endpoint a_query！", record)
        return muti_table_add_record(app_id=app_id, table_id=table_id, record=record)

    # 后置处理
    async def a_lark_after_notify(self, receive_id: str, text: str):
        return send_message(receive_id, text)
