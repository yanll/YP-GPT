import asyncio
import json
import logging
from typing import Dict, List, Optional, Union

from dbgpt.agent.actions.action import ActionOutput
from dbgpt.agent.actions.calendar_action import CalendarAction
from dbgpt.agent.resource.resource_api import ResourceType, ResourceClient
from dbgpt.agent.resource.resource_lark_api import ResourceLarkClient
from dbgpt.util.error_types import LLMChatError
from ..base_agent_new import ConversableAgent
from dbgpt.agent.memory.base import MyGptsConversation
import time

logger = logging.getLogger(__name__)


class CalendarAssistantAgent(ConversableAgent):
    name = "Yang"
    profile: str = "CalendarAssistant"
    goal: str = ("引导我输入预定会议室所需的信息，包括参会人数和会议的开始结束时间为我推荐最合适的会议室预定方案，最后将推荐的会议室按照格式要求回复给我。\n"
                 "1、这是全部会议室数据：\n\tall_meeting_rooms={all_meeting_rooms}\n\tall_meeting_rooms：{meeting_room_field_common}\n"
                 "2、当前系统时间是：{current_time}\n"
                 "3、常用时间描述的含义：上午代表10-12点，下午代表14-16点\n"
                 "")

    constraints: List[str] = [
        "你是一个数据分析专家，也是一个会议室预定助手，目标是根据我的输入，引导我输入预定会议室所需的信息，包括会议的开始结束时间。",
        "预定会议室必须明确会议室使用的开始和结束时间，这一项不能没有。",
        "请注意会议开始和结束时间按照Python语法中的“%Y-%m-%d %H:%M:%S”格式解析。",
        "请根据已有的会议室引导我选择哪个会议室，包括输入会议开始时间和结束时间。",
        "请根据我的输入结合全部会议室的属性，为我推荐我合适预定的会议室。",
        "必须在我给定的全部会议室中推荐，不要给我推荐不存在的会议室，推荐的会议室根据all_meeting_rooms中的数据得出。",
        "如果我直接输入了要预定的会议室和时间段，优先按照我的输入处理。",
        "为我展示会议室清单和详细信息时，整理后再展示，尽量美观直观。",
        "开始和结束时间根据我输入的时间推理，结合当前系统时间计算出精确时间。",
        "我询问关于会议室的信息时，请分析all_meeting_rooms中的数据，为我提供正确的答案。",
        "如果最终确定了会议室和时间，总结我选择的会议室和时间，务必按照我要求的格式输出结果。",
        "当我输入“Y”时，按照我要求的格式返回结果，如果结果不是按格式返回的，请继续思考直到返回结果达到要求。",
    ]
    desc: str = "引导我预定合适的会议室"
    max_retry_count: int = 1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_actions([CalendarAction])

    def _init_reply_message(self, recive_message):
        resesource_api: ResourceClient = self.resource_loader.get_resesource_api(resource_type=ResourceType.LarkApi)
        reply_message = super()._init_reply_message(recive_message)
        reply_message["context"] = {
            "all_meeting_rooms": resesource_api.get_all_meeting_rooms(),
            "meeting_room_field_common": '{"capacity": "会议室最大可容纳人数", "floor_name": "会议室所在楼层", "name": "会议室名字",  "room_id": "会议室ID"}',
            "current_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            # "meeting_rooms_status": resesource_api.get_meeting_room_status(),
        }
        print("日历消息模版内容：", reply_message)
        return reply_message

    async def a_correctness_check(self, message: Optional[Dict]):
        action_reply = message.get("action_report", None)
        if action_reply is None:
            return (
                False,
                f"No executable analysis Calendar is generated,{message['content']}.",
            )
        action_out = ActionOutput.from_dict(action_reply)
        if action_out.is_exe_success == False:
            return (
                False,
                f"Please check your answer, {action_out.content}.",
            )
        try:
            resource_lark_client: ResourceLarkClient = (
                self.resource_loader.get_resesource_api(
                    ResourceType(action_out.resource_type)
                )
            )

            result = await resource_lark_client.a_lark_after_notify(
                receive_id="liangliang.yan@yeepay.com",
                text="\n已将日历提交到飞书，请查看结果！"
            )
            print('CalendarAssistantAgent处理结果：', result)
            if (result['code'] == 0):
                logger.info("代理任务执行成功！")
                delete_last: MyGptsConversation = self.memory.my_conversation_memory.disable_con_by_conv_id(
                    conv_id=self.agent_context.conv_id
                )
                return (
                    True, None
                )
            else:
                logger.error("代理任务执行失败，请检查飞书接口调用日志！")
                return (
                    False,
                    "请检查飞书接口调用日志！",
                )
        except Exception as e:
            logger.exception(f"DataScientist check exception！{str(e)}")
            return (
                False,
                f"Lark execution error, please re-read the historical information to fix this API. The error message is as follows:{str(e)}",
            )

    async def a_thinking(
            self,
            messages: Optional[List[Dict]],
            his_human_messages: Optional[List[Dict]] = None,
            prompt: Optional[str] = None
    ) -> Union[str, Dict, None]:
        last_model = None
        last_err = None
        retry_count = 0
        conv_uid = self.agent_context.conv_id.split("_")[0]
        convs = self.memory.my_conversation_memory.get_cons_by_conv_uid(
            conv_uid=conv_uid
        )
        # 替换原有消息，将历史记录传入GPT
        if True:
            messages = []
            for conv in convs:
                messages.append({
                    "role": 'human',
                    "content": conv.user_goal,
                    "context": None
                })

        while retry_count < 3:
            llm_model = await self._a_select_llm_model(last_model)
            try:
                if prompt:
                    messages = self._new_system_message(prompt) + messages
                else:
                    messages = self.oai_system_message + messages

                response = await self.llm_client.create(
                    context=messages[-1].pop("context", None),
                    messages=messages,
                    llm_model=llm_model,
                    max_new_tokens=self.agent_context.max_new_tokens,
                    temperature=self.agent_context.temperature,
                )
                return response, llm_model
            except LLMChatError as e:
                logger.error(f"model:{llm_model} generate Failed!{str(e)}")
                retry_count += 1
                last_model = llm_model
                last_err = str(e)
                await asyncio.sleep(10)

        if last_err:
            raise ValueError(last_err)
