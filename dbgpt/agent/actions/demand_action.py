import json
import logging
from typing import Optional

from pydantic import BaseModel, Field

from dbgpt.agent.actions.action import ActionOutput, T
from dbgpt.agent.resource.resource_api import AgentResource, ResourceType
from dbgpt.agent.resource.resource_db_api import ResourceDbClient
from dbgpt.agent.resource.resource_lark_api import ResourceLarkClient
from dbgpt.vis.tags.vis_chart import Vis, VisChart

from .action import Action

logger = logging.getLogger(__name__)


class LarkInput(BaseModel):
    display_type: str = Field(
        ...,
        description="The chart rendering method selected for SQL. If you don’t know what to output, just output 'response_table' uniformly.",
    )
    sql: str = Field(
        ..., description="Executable sql generated for the current target/problem"
    )
    demand: str = Field(
        ..., description="飞书项目需要接收的需求内容"
    )
    thought: str = Field(..., description="Summary of thoughts to the user")


class DemandAction(Action[LarkInput]):
    def __init__(self):
        self._render_protocal = VisChart()

    @property
    def resource_need(self) -> Optional[ResourceType]:
        return ResourceType.LarkApi

    @property
    def render_protocal(self) -> Optional[Vis]:
        return self._render_protocal

    @property
    def out_model_type(self):
        return LarkInput

    async def a_run(
            self,
            ai_message: str,
            resource: Optional[AgentResource] = None,
            rely_action_out: Optional[ActionOutput] = None,
            need_vis_render: bool = True,
    ) -> ActionOutput:
        try:
            param: LarkInput = self._input_convert(ai_message, LarkInput)
        except Exception as e:
            logger.exception(f"str(e)! \n {ai_message}")
            return ActionOutput(
                is_exe_success=False,
                content="The requested correctly structured answer could not be found.",
            )
        try:
            resource_db_client: ResourceLarkClient = (
                self.resource_loader.get_resesource_api(self.resource_need)
            )
            if not resource_db_client:
                raise ValueError(
                    "There is no implementation class bound to database resource execution！"
                )
            print("此处根据AI返回的结果执行下一步动作：调用外部接口", resource, param)
            data_df = await resource_db_client.a_query_to_df(resource.value, param.sql)
            view = await self.render_protocal.display(
                chart=json.loads(param.json()), data_df=data_df
            )
            return ActionOutput(
                is_exe_success=True,
                content=param.json(),
                view=view,
                resource_type=self.resource_need.value,
                resource_value=resource.value,
            )
        except Exception as e:
            logger.exception("Check your answers, the sql run failed！")
            return ActionOutput(
                is_exe_success=False,
                content=f"Check your answers, the sql run failed!Reason:{str(e)}",
            )
