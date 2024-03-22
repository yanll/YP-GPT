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
        "请客观真实的识别用户输入，按照：{fields} 拆解出来，不要生成用户没有输入的内容，不要随意编造信息。",
        "如果用户输入的信息不含“需求内容”关键字段，提醒用户按照正确的格式输入需求。",
        "如果用户输入的信息不含“紧急程度”关键字段，按照“一般紧急”提取。",
        "如果用户输入的信息太少或没有提取到有用信息，提醒用户输入更详细的内容。",
    ]
    desc: str = "使用用户提供的关键字段信息提取"
    max_retry_count: int = 1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_actions([DemandAction])

    def _init_reply_message(self, recive_message):
        reply_message = super()._init_reply_message(recive_message)
        reply_message["context"] = {
            "display_type": "需求要点",
            "fields": "[需求内容,紧急程度]"
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
        sql = action_reply_obj.get("sql", None)
        if not sql:
            return (
                False,
                "Please check your answer, the sql information that needs to be generated is not found.",
            )
        try:
            resource_db_client: ResourceLarkClient = (
                self.resource_loader.get_resesource_api(
                    ResourceType(action_out.resource_type)
                )
            )

            columns, values = await resource_db_client.a_query(
                db=action_out.resource_value, sql=sql
            )
            print('执行SQL：', columns, sql)
            print('SQL执行结果：', values)
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
