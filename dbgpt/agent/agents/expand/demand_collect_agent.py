import asyncio
import json
import logging
from typing import Dict, List, Optional, Union

from dbgpt.agent.actions.action import ActionOutput
from dbgpt.agent.actions.demand_action import DemandAction
from dbgpt.agent.resource.resource_api import ResourceType
from dbgpt.agent.resource.resource_lark_api import ResourceLarkClient
from dbgpt.util.error_types import LLMChatError
from ..base_agent_new import ConversableAgent

logger = logging.getLogger(__name__)


# a_generate_reply
# ----a_act
# --------a_run
# ----a_verify
# --------a_correctness_check
# ------------a_muti_table_add_record

# a_act: 组装大模型，返回结果。
# a_run: 根据大模型结果调用外部，1、初步执行外部操作 2、调用展示组件。
# a_verify: 校验大模型返回结果，最后调用a_correctness_check
# a_correctness_check：后置处理

class ProductionAssistantAgent(ConversableAgent):
    name = "Listen"
    profile: str = "ProductionAssistant"
    goal: str = "提取用户输入信息中的需求点并按字段要求拆解，最后将拆解后的信息按格式返回。"
    constraints: List[str] = [
        "注意你是一个需求收集助手，目标是提取信息，不用真的帮用户实现需求。",
        "请仔细理解用户输入，客观真实的识别，按照：{fields} 将用户输入的内容拆解出来。",
        "需求必须是有意义的内容，包含并不限于用户的痛点、槽点、需求、期望、愿景等。",
        "需求要明确客观，不随意编造内容。紧急程度根据用户的输入的语义判断级别，按照【“非常紧急”，“比较紧急”，“不紧急”】处理。期望完成时间尽量提取准确的时间信息。",
        "如果用户输入的信息太少或没有提取到有用信息，提醒用户输入更详细的内容。",
        "如果没有提取到“需求内容”信息，按照“”处理并提醒用户输入。",
        "如果没有提取到“期望完成时间”信息，按照“”处理并提醒用户输入",
        "如果没有提取到“紧急程度”信息，按照“比较紧急”处理。",
        "回复的内容不要包含情绪、主观思维信息。",
    ]
    desc: str = "提取用户输入中的 {fields} 信息”"
    max_retry_count: int = 1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_actions([DemandAction])

    def _init_reply_message(self, recive_message):
        reply_message = super()._init_reply_message(recive_message)
        reply_message["context"] = {
            "fields": "[“需求内容”,“紧急程度”,“期望完成时间”]"
        }
        print("需求收集代理回复消息模版内容：", reply_message)
        return reply_message

    async def a_correctness_check(self, message: Optional[Dict]):
        action_reply = message.get("action_report", None)
        if action_reply is None:
            return (
                False,
                f"No executable analysis Demand is generated,{message['content']}.",
            )
        action_out = ActionOutput.from_dict(action_reply)
        if action_out.is_exe_success == False:
            return (
                False,
                f"Please check your answer, {action_out.content}.",
            )
        action_reply_obj = json.loads(action_out.content)
        demand = action_reply_obj.get("demand", None)
        if not demand:
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
                text="\n已将需求内容提交到飞书，请查看结果！\n\n需求内容：" + demand
            )
            print('ProductionAssistantAgent处理结果：', result)
            if (result['code'] == 0):
                logger.info("代理任务执行成功！")
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
        messages = his_human_messages if his_human_messages is not None and his_human_messages != [] else messages
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
