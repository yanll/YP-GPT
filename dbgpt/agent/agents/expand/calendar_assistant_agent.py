import asyncio
import json
import logging
from typing import Dict, List, Optional, Union

from dbgpt.agent.actions.action import ActionOutput
from dbgpt.agent.actions.calendar_action import CalendarAction
from dbgpt.agent.resource.resource_api import ResourceType
from dbgpt.agent.resource.resource_lark_api import ResourceLarkClient
from dbgpt.util.error_types import LLMChatError
from ..base_agent_new import ConversableAgent
from dbgpt.agent.memory.base import MyGptsConversation
from dbgpt.serve.agent.db.gpts_conversations_db import GptsConversationsDao, GptsConversationsEntity
import time
logger = logging.getLogger(__name__)


class CalendarAssistantAgent(ConversableAgent):
    name = "Yang"
    profile: str = "CalendarAssistant"
    goal: str = ("根据提供的会议室信息（包括可预定时间、所在楼层、可容纳人数、忙闲状态等）为我推荐最合适的会议室预定方案\n"
                 "1、这是全部会议室数据：all_rooms={all_rooms}，all_rooms字段含义是：{room_field_common}\n"
                 "2、这是忙碌状态的会议室：\n"
                 "3、当前的时间是：{current_time}")
    constraints: List[str] = [
        "必须按照我提供的格式返回。",
        "首先你具备通用AI助手的能力，不要作出奇怪的回答。",
        "如果我不想继续了，提醒我可以随时继续提问。",
        "如果类似的信息我多次输入，以最后输入的为准。",
        "注意你是一个需求内容专家，目标是提取信息，如果提取不到有用的信息，告诉我你能做什么。",
        "请仔细理解我的输入，客观真实的识别，按照：{fields} 将我输入的内容拆解出来。",
        "需求必须是有意义的内容，包含并不限于我的痛点、槽点、需求、期望、愿景等,不要改变我的需求内容。",
        "需求要明确客观，不随意编造内容。紧急程度根据我的输入的语义判断级别，按照【“非常紧急”，“比较紧急”，“不紧急”】处理。期望完成时间尽量提取准确的时间信息。",
        "如果我输入的信息太少或没有提取到有用信息，提醒我输入更详细的内容。",
        "如果没有提取到“需求内容”信息，按照“”处理并提醒我输入“需求内容”，不要胡乱编造需求。",
        "提取的“需求内容”至少10个字以上，否则按照“”处理并提醒我输入更详细的“需求内容”，不要胡乱处理。",
        "如果没有提取到“期望完成时间”信息，按照“”处理并提醒我输入“期望完成时间”，不要胡乱编造时间",
        "如果没有提取到“紧急程度”信息，按照“比较紧急”处理，不要胡乱处理。",
        "如果没有提取到“是否确认提交”信息，按照“”处理，不要胡乱处理，不用提醒我输入。",
        "“是否确认提交”要客观明确，根据上下文和我输入的语义判断，不要随意编造结果，只能按照【“是”，“否”】处理。",
        "如果无法理解我输入的信息，按照通用AI回复并告诉我你能做什么，引导我正确的输入。",
        "回复的内容不要包含情绪、主观思维信息。",

    ]
    desc: str = "提取输入中的 {fields} 信息”"
    max_retry_count: int = 1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_actions([CalendarAction])

    def _init_reply_message(self, recive_message):
        reply_message = super()._init_reply_message(recive_message)
        reply_message["context"] = {
            "all_rooms": '[{"capacity": 12,"floor_name": "F10","name": "Hacker","room_id": "omm_fce8075d5a6a25c764a808c69a48b82a"},{"capacity": 8,"floor_name": "F25","name": "smart","room_id": "omm_435bca3a3d40f120c63540028b965538"},{"capacity": 10,"floor_name": "F25","name": "think different","room_id": "omm_d511e9e4e40f68107f556c943ca50c44"},{"capacity": 90,"floor_name": "F23","name": "分享","room_id": "omm_2fa172ec56aba79c654ec5a4b58e9f27"},{"capacity": 12,"floor_name": "F10","name": "北极星","room_id": "omm_3864b3539c370d51e8d086791b008d44"},{"capacity": 8,"floor_name": "F10","name": "坦诚","room_id": "omm_247693a0dbb368b6af624c51ba5df218"},{"capacity": 4,"floor_name": "F10","name": "天权星","room_id": "omm_32be015ee6d9318e11561b984d665971"},{"capacity": 5,"floor_name": "F10","name": "天枢星","room_id": "omm_dcf65c2ffcbabe4bf01c72e0470c541b"},{"capacity": 7,"floor_name": "F10","name": "天狼星","room_id": "omm_7e99a24f850323e3038526ce3f809ba5"},{"capacity": 4,"floor_name": "F10","name": "天玑星","room_id": "omm_fecbfd6505548d491026365ad03cb215"},{"capacity": 5,"floor_name": "F10","name": "天璇星","room_id": "omm_ddee0861011df191f0404b80f0c7d9eb"},{"capacity": 5,"floor_name": "F10","name": "天衡星","room_id": "omm_e457d7a3eb7133f98fc27a267a1646c1"},{"capacity": 10,"floor_name": "F23","name": "太阳","room_id": "omm_d47dd4f223a3531f31b351513b036f61"},{"capacity": 31,"floor_name": "F23","name": "尽责","room_id": "omm_41510695cc2c9e86c3ef7d4afc247c74"},{"capacity": 6,"floor_name": "F23","name": "开放","room_id": "omm_9da759bfae9935249eda2ce675e2682e"},{"capacity": 6,"floor_name": "F10","name": "开阳星","room_id": "omm_56bb92f696093b60a3108ae3b7102a78"},{"capacity": 6,"floor_name": "F10","name": "摇光星","room_id": "omm_2db12593ce9242345be73a59a0120ccc"},{"capacity": 7,"floor_name": "F25","name": "敢干","room_id": "omm_4a260a86bc05a2d7dbb901c53bf5bc92"},{"capacity": 5,"floor_name": "F10","name": "敢想","room_id": "omm_001832945aef034f5853ca649db51b97"},{"capacity": 15,"floor_name": "F10","name": "敢说","room_id": "omm_5a1d13dc13e79e6f739b3d6f2d26c452"},{"capacity": 10,"floor_name": "F25","name": "敢败","room_id": "omm_1898ce77b933009c84cc999a93aeefc4"},{"capacity": 8,"floor_name": "F25","name": "极致","room_id": "omm_a77aef5161de2d637bc0c156647474d4"},{"capacity": 4,"floor_name": "F10","name": "泰山","room_id": "omm_bb38d0046d5159a31385030a1346a6c5"},{"capacity": 12,"floor_name": "F10","name": "浪漫","room_id": "omm_a5ec3a14a94322968cd6fea05b34f4df"},{"capacity": 6,"floor_name": "F23","name": "禾口","room_id": "omm_e8f296a80f0f448a9d6c659abb0a7ea8"},{"capacity": 6,"floor_name": "F23","name": "蓝点","room_id": "omm_c520c17858b4b6fb22bac99f6e1dda5b"},{"capacity": 5,"floor_name": "F10","name": "超越","room_id": "omm_9ca36d25bfe178df5da26205b39da278"}]',
            "room_field_common": '{"capacity": "会议室最大可容纳的人数", "floor_name": "会议室所在的楼层", "name": "会议室的名字",  "room_id": "会议室的ID"}',
            "current_time":time.strftime("")
        }
        print("需求收集代理回复消息模版内容：", reply_message)
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
        action_reply_obj = json.loads(action_out.content)
        calendar = action_reply_obj.get("calendar", None)
        if not calendar:
            return (
                False,
                "请检查您的问题，生成的内容中没有找到需求信息！",
            )
        try:
            resource_lark_client: ResourceLarkClient = (
                self.resource_loader.get_resesource_api(
                    ResourceType(action_out.resource_type)
                )
            )

            result = await resource_lark_client.a_lark_after_notify(
                receive_id="liangliang.yan@yeepay.com",
                text="\n已将需求内容提交到飞书，请查看结果！\n\n需求内容：" + calendar
            )
            print('CalendarAssistantAgent处理结果：', result)
            if (result['code'] == 0):
                logger.info("代理任务执行成功！")
                # 删除最后一条确认消息（TODO-YLL-FIXME：删除全部会话）
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
