import json
import logging
from typing import Optional

from pydantic import BaseModel, Field

from dbgpt.agent.actions.action import ActionOutput
from dbgpt.agent.resource.resource_api import AgentResource, ResourceType
from dbgpt.agent.resource.resource_lark_api import ResourceLarkClient
from dbgpt.vis.tags.vis_demand import Vis, VisDemand
from .action import Action

logger = logging.getLogger(__name__)


class LarkInput(BaseModel):
    display_type: str = Field(
        description="The chart rendering method selected for SQL. If you don’t know what to output, just output 'response_table' uniformly.",
    )
    urgency: str = Field(
        ..., description="提取的“紧急程度”信息"
    )
    demand: str = Field(
        ..., description="提取的“需求”信息"
    )
    pre_time: str = Field(
        ..., description="提取的“期望完成时间”信息"
    )
    thought: str = Field(..., description="Summary of thoughts to the user")


class DemandAction(Action[LarkInput]):
    def __init__(self):
        self._render_protocal = VisDemand()

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
            aimdict = eval(ai_message)
            if "display_type" not in aimdict:
                aimdict["display_type"] = ""
            if "urgency" not in aimdict:
                aimdict["urgency"] = ""
            if "demand" not in aimdict:
                aimdict["demand"] = ""
            if "pre_time" not in aimdict:
                aimdict["pre_time"] = ""
            if "thought" not in aimdict:
                aimdict["thought"] = ""

            if aimdict["demand"] == "":
                return ActionOutput(
                    is_exe_success=False,
                    content="未识别到需求信息，请重新输入！",
                )
            param: LarkInput = self._input_convert(json.dumps(aimdict), LarkInput)
        except Exception as e:
            logger.exception(f"格式转换异常：str(e)! \n {ai_message}")
            return ActionOutput(
                is_exe_success=False,
                content="The requested correctly structured answer could not be found.",
            )
        try:
            resource_lark_client: ResourceLarkClient = (
                self.resource_loader.get_resesource_api(self.resource_need)
            )
            if not resource_lark_client:
                raise ValueError(
                    "There is no implementation class bound to database resource execution！"
                )
            print("此处根据AI返回的结果执行下一步动作：调用外部接口", resource, param)
            result = await resource_lark_client.a_muti_table_add_record(
                app_id="NorvbogbxaCD4VsMrLlcTzv0nTe",
                table_id="tblG1alED3YxCJua",
                record={
                    "fields": {
                        "需求内容": param.demand,
                        "紧急程度": param.urgency,
                        "期望完成时间": param.pre_time,
                        "创建人": "",
                        "创建时间": ""
                    }
                }
            )
            view = await self.render_protocal.display(content=param, add_result=result)
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
