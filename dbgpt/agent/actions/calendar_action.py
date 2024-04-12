import json
import logging
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Union,
)

from pydantic import BaseModel, Field

from dbgpt.agent.actions.action import ActionOutput
from dbgpt.agent.resource.resource_api import AgentResource, ResourceType
from dbgpt.agent.resource.resource_lark_api import ResourceLarkClient
from dbgpt.vis.tags.vis_calendar import Vis, VisCalendar
from .action import Action

logger = logging.getLogger(__name__)


class LarkInput(BaseModel):
    name: str = Field(
        ..., description="会议室名字"
    )
    capacity: str = Field(
        ..., description="会议室最大可容纳人数"
    )
    floor_name: str = Field(
        ..., description="会议室所在楼层"
    )
    start_time: str = Field(
        ..., description="会议开始时间"
    )
    end_time: str = Field(
        ..., description="会议结束时间"
    )
    confirm: str = Field(
        ..., description="提取的“是否确认预定”信息"
    )
    ai_message: str = Field(
        ..., description="Summary of thoughts to the user"
    )


class CalendarAction(Action[LarkInput]):
    def __init__(self):
        self._render_protocal = VisCalendar()

    @property
    def ai_out_schema(self) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        if self.out_model_type is None:
            return None

        return f"""必须按照以下格式响应:
                        {json.dumps(self._create_example(self.out_model_type), indent=2, ensure_ascii=False)}
                    Make sure the response is correct json and can be parsed by Python json.loads. 
                    """

    @property
    def resource_need(self) -> Optional[ResourceType]:
        return ResourceType.LarkApi

    @property
    def render_protocal(self) -> Optional[Vis]:
        return self._render_protocal

    @property
    def out_model_type(self):
        return LarkInput

    async def run(
            self,
            ai_message: str,
            resource: Optional[AgentResource] = None,
            rely_action_out: Optional[ActionOutput] = None,
            need_vis_render: bool = True,
    ) -> ActionOutput:
        try:
            print("AI Response Message：", ai_message)

            if (ai_message.startswith("{")):
                aimdict = eval(ai_message)
            else:
                return ActionOutput(is_exe_success=False, content=ai_message)

            param: LarkInput = self._input_convert(json.dumps(aimdict), LarkInput)
        except Exception as e:
            logger.exception(f"格式转换异常：str(e)! \n\n {ai_message}")
            return ActionOutput(
                is_exe_success=False,
                content="The requested correctly structured answer could not be found.",
            )
        try:
            resource_lark_client: ResourceLarkClient = (
                self.resource_loader.get_resource_api(self.resource_need)
            )
            if not resource_lark_client:
                raise ValueError(
                    "There is no implementation class bound to lark resource execution！"
                )
            print("此处根据AI返回的结果执行下一步动作：调用外部接口", resource, param)
            room_id = ''
            all = json.loads(resource_lark_client.get_all_meeting_rooms())
            for r in all:
                if r['name'] == param.name:
                    room_id = r['room_id']
                    break

            result = await resource_lark_client.create_calendar(
                title="我的测试日程",
                name=param.name,
                room_id=room_id,
                start_time=param.start_time,
                end_time=param.end_time
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
            logger.exception("检查飞书日历接口执行！")
            return ActionOutput(
                is_exe_success=False,
                content=f"Check your answers, the lark run failed!Reason:{str(e)}",
            )
