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
    urgency: str = Field(
        ..., description="提取的“紧急程度”信息"
    )
    pre_time: str = Field(
        ..., description="提取的“期望完成时间”信息"
    )
    confirm: str = Field(
        ..., description="提取的“是否确认提交”信息"
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

        return f"""Please response in the following json format:
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

    async def a_run(
            self,
            ai_message: str,
            resource: Optional[AgentResource] = None,
            rely_action_out: Optional[ActionOutput] = None,
            need_vis_render: bool = True,
    ) -> ActionOutput:
        try:
            print("AI Response Message：", ai_message)
            aimdict = {}

            if (ai_message.startswith("{")):
                aimdict = eval(ai_message)
            else:
                return ActionOutput(is_exe_success=False, content=ai_message)

            if "ai_message" not in aimdict:
                aimdict["ai_message"] = ""


            info = ("#### ai_message：" + aimdict["ai_message"] + '\n\n' +
                    '#### \n\n' +
                    '紧急程度：' + aimdict["urgency"] + '\n\n' +
                    '期望完成时间：' + aimdict["pre_time"] + '\n\n' +
                    '#### \n\n'
                    )

            if aimdict["pre_time"] == "":
                return ActionOutput(is_exe_success=False, content=info + '\n\n #### 请输入期望完成时间！')
            if (aimdict["confirm"] != "是"):
                return ActionOutput(
                    is_exe_success=False,
                    content=info + '\n\n #### 是否确认将以上信息提交到飞书？您也可以继续输入修改以上内容！'
                )
            param: LarkInput = self._input_convert(json.dumps(aimdict), LarkInput)
        except Exception as e:
            logger.exception(f"格式转换异常：str(e)! \n\n {ai_message}")
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
