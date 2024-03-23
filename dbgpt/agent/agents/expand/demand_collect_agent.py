import json
import logging
from typing import Callable, Dict, List, Literal, Optional, Union

from dbgpt.agent.actions.action import ActionOutput
from dbgpt.agent.actions.demand_action import DemandAction
from dbgpt.agent.resource.resource_api import ResourceType
from dbgpt.agent.resource.resource_db_api import ResourceDbClient
from dbgpt.agent.resource.resource_lark_api import ResourceLarkClient

from ..base_agent_new import ConversableAgent

logger = logging.getLogger(__name__)


class ProductionAssistantAgent(ConversableAgent):
    name = "Listen"
    profile: str = "ProductionAssistant"
    goal: str = "你是一个需求收集助理，你的目标是提取用户输入信息中的需求点并按字段要求拆解，并将拆解后的信息按格式返回。你的目的是收集需求，不用真的帮用户实现需求。"
    constraints: List[str] = [
        "请仔细理解用户输入，客观真实的识别，按照：{fields} 将用户输入的内容拆解出来。",
        "需求要明确客观，不随意编造内容。紧急程度根据用户的输入的语义判断级别，按照【“非常紧急”，“比较紧急”，“不紧急”】处理。期望完成时间尽量提取准确的时间信息。",
        "如果用户输入的信息不含“需求内容”信息，提醒用户按照正确的格式输入需求。",
        "如果用户输入的信息不含“紧急程度”信息，按照“一般紧急”处理。",
        "如果用户输入的信息不含“期望完成时间”信息，按照“排期推进”处理。",
        "如果用户输入的信息太少或没有提取到有用信息，提醒用户输入更详细的内容。",
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
            "display_type": "text",
            "fields": "[“需求内容”,“紧急程度”,“期望完成时间”]"
        }
        print("需求收集代理回复消息：", reply_message)
        return reply_message

    async def a_correctness_check(self, message: Optional[Dict]):
        action_reply = message.get("action_report", None)
        if action_reply is None:
            return (
                False,
                f"No executable analysis SQL is generated,{message['content']}.",
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

            # columns, values = await resource_lark_client.a_query(
            #     db=action_out.resource_value, sql=demand
            # )
            columns, values = (
                [], []
            )
            print('执行调用：', columns, demand)
            print('执行调用结果：', values)
            if not values or len(values) <= 0:
                return (
                    False,
                    "Please check your answer, the current SQL cannot find the data to determine whether filtered field values or inappropriate filter conditions are used.",
                )
            else:
                logger.info(
                    f"reply check success! There are {len(values)} rows of data"
                )
                return True, None
        except Exception as e:
            logger.exception(f"DataScientist check exception！{str(e)}")
            return (
                False,
                f"SQL execution error, please re-read the historical information to fix this SQL. The error message is as follows:{str(e)}",
            )
