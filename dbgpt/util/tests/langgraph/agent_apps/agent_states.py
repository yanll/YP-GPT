import operator
from typing import TypedDict, Dict, Union, Annotated

from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.messages import BaseMessage


class GeneralAgentState(TypedDict):
    input: str
    chat_history: list[BaseMessage]
    # 代理的调用结果
    # 需要将`None`作为有效类型，因为这将作为初始值
    agent_outcome: Union[AgentAction, AgentFinish, None]
    # 操作和相应观察结果的列表
    # 在此处我们使用`operator.add`进行注释，以指示对此状态的操作应该被添加到现有值中而不是覆盖它
    intermediate_steps: Annotated[list[tuple[AgentAction, str]], operator.add]
