import json
import operator
import os
from typing import TypedDict, Union, Annotated, Dict, Optional

from langchain.agents import create_openai_functions_agent
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.messages import BaseMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, SystemMessagePromptTemplate, \
    HumanMessagePromptTemplate, PromptTemplate
from langchain_core.utils.function_calling import convert_to_openai_tool
from langgraph.graph import END, StateGraph
from langgraph.prebuilt import ToolExecutor

from dbgpt.util.azure_util import create_azure_llm
from dbgpt.util.tests.langgraph.tools.dmall_tool import DmallSearchResults

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "ls__19718564013e408d8d5ae23ad8dbdf29"


class AgentState(TypedDict):
    # 输入字符串
    input: str
    # api_name: str
    # api_version: str
    # api_parameters: str
    # 会话中以前的消息列表
    chat_history: list[BaseMessage]
    # 给定对代理的调用的结果
    # 需要将`None`作为有效类型，因为这将作为初始值
    agent_outcome: Union[AgentAction, AgentFinish, None]
    # 操作和相应观察结果的列表
    # 在此处我们使用`operator.add`进行注释，以指示对此状态的操作应该被添加到现有值中（而不是覆盖它）
    intermediate_steps: Annotated[list[tuple[AgentAction, str]], operator.add]


template = '''Answer the following questions as best you can. You have access to the following tools:

                    {tools}

                    Please answer in simplified Chinese.

                    Use the following format:

                    Question: the input question you must answer
                    Thought: you should always think about what to do
                    Action: the action to take, should be one of [{tool_names}]
                    Action Input: the input to the action
                    Observation: the result of the action
                    ... (this Thought/Action/Action Input/Observation can repeat N times)
                    Thought: I now know the final answer
                    Final Answer: the final answer to the original input question

                    Begin!

                    Question: {input}
                    Thought:{agent_scratchpad}'''

chat_prompt = PromptTemplate.from_template(template)


tools = [DmallSearchResults(max_results=20)]
# tools = [convert_to_openai_tool(DmallSearchResults(max_results=20))]
tool_names = ["dmall_search_results_json"]
print("tools:\n", [convert_to_openai_tool(DmallSearchResults(max_results=20))])
prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(template="You are a helpful assistant"),
        MessagesPlaceholder(variable_name="chat_history", optional=True),
        HumanMessagePromptTemplate.from_template(template="{input}"),
        # HumanMessagePromptTemplate.from_template(template="{api_name}"),
        # HumanMessagePromptTemplate.from_template(template="{api_version}"),
        # MessagesPlaceholder(variable_name="api_parameters"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ]
)

# 选择将驱动代理的LLM
llm = create_azure_llm()

# 构建OpenAI函数代理
agent_runnable = create_openai_functions_agent(llm, tools, prompt)
# agent_runnable = create_openai_functions_agent(llm, tools, chat_prompt)

# 这是我们的一个有用的辅助类，用于运行工具
# 它接受代理操作并调用该工具，然后返回结果
tool_executor = ToolExecutor(tools)


# 定义代理
def run_agent(data):
    agent_outcome = agent_runnable.invoke(data)
    return {"agent_outcome": agent_outcome}


# 定义执行工具的函数
def execute_tools(data):
    # 获取最近的代理操作 - 这是在上述`agent`中添加的关键字
    agent_action = data["agent_outcome"]
    output = tool_executor.invoke(agent_action)
    return {"intermediate_steps": [(agent_action, str(output))]}


# 定义将用于确定要继续的条件边的逻辑
def should_continue(data):
    # 如果代理结果是AgentFinish，则返回`exit`字符串
    # 这将在设置图形以定义流程时使用
    if isinstance(data["agent_outcome"], AgentFinish):
        return "end"
    # 否则，将返回AgentAction
    # 在这里我们返回`continue`字符串
    # 这将在设置图形以定义流程时使用
    else:
        return "continue"


# 定义一个新的图形
workflow = StateGraph(AgentState)

# 定义我们将循环的两个节点
workflow.add_node("agent", run_agent)
workflow.add_node("action", execute_tools)

# 将入口点设置为`agent`
# 这意味着这个节点是第一个被调用的
workflow.set_entry_point("agent")

# 现在我们添加一个条件边
workflow.add_conditional_edges(
    # 首先，我们定义起始节点。我们使用`agent`。
    # 这意味着这些是在调用`agent`节点后采取的边。
    "agent",
    # 接下来，我们传入将决定接下来调用哪个节点的函数。
    should_continue,
    # 最后我们传入一个映射。
    # 键是字符串，值是其他节点。
    # END是一个特殊的节点，表示图形应该结束。
    # 将发生的是我们将调用`should_continue`，然后将其输出与此映射中的键进行匹配。
    # 根据匹配结果，然后将调用该节点。
    {
        # 如果是`tools`，那么我们调用工具节点。
        "continue": "action",
        # 否则我们结束。
        "end": END,
    },
)

# 现在，我们从`tools`到`agent`添加了一个普通边缘。
# 这意味着在调用`tools`之后，将调用`agent`节点。
workflow.add_edge("action", "agent")

# 最后，我们进行编译！
# 这将其编译为LangChain Runnable，
# 这意味着您可以像使用任何其他可运行文件一样使用它
app = workflow.compile()

inputs = {
    # "tools": tools,
    # "tool_names": tool_names,
    # "input": "帮我定个会议室，明天2点，4个人参加",
    "input": "帮我查询毛利大于10000的商户",
    # "input": "你好",
    "chat_history": [],
    # "chat_history": [{
    #     "role": "human",
    #     "content": "查询编号为123456的商户"
    # }],
    # "api_name": "query_merchant_info",
    # "api_version": "V1.0",
    # "api_parameters": ["123456"]
}
for s in app.stream(inputs):
    print(list(s.values())[0])
    print("----")

# app = chat_agent_executor.create_function_calling_executor(llm, tools)
# app.get_graph().print_ascii()
