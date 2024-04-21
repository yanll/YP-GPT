import json
import os
from typing import Any, Dict, List

from langchain.agents import create_openai_functions_agent
from langchain_core.agents import AgentFinish
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, SystemMessagePromptTemplate, \
    HumanMessagePromptTemplate, PromptTemplate
from langgraph.graph import END, StateGraph
from langgraph.graph.graph import CompiledGraph
from langgraph.prebuilt import ToolExecutor, ToolInvocation

from dbgpt.extra.cache.redis_cli import RedisClient
from dbgpt.util.azure_util import create_azure_llm
from dbgpt.util.tests.langgraph.agent_apps.agent_states import GeneralAgentState
from dbgpt.util.tests.langgraph.agent_apps.tools_provider import ToolsProvider

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "ls__19718564013e408d8d5ae23ad8dbdf29"

# 选择将驱动代理的LLM
llm = create_azure_llm()
tools_provider = ToolsProvider()

template = '''Answer the following questions as best you can. You have access to the following tools:

                    {tools}

                    Please answer in simplified Chinese.

                    Use the following format:

                    Question: the input question you must answer
                    Thought: you should always think about what to do
                    Action: the action to take, should be one of [{tool_names}]
                    Action Input: the input to the action, must be extract from Question, fabrication is prohibited.
                    Observation: the result of the action
                    ... (this Thought/Action/Action Input/Observation can repeat 2 times)
                    Thought: I now know the final answer
                    Final Answer: the final answer to the original input question

                    Begin!
                    HistoryQuestion：{chat_history}：
                    Question: {input}
                    Thought:{agent_scratchpad}'''

chat_prompt = ChatPromptTemplate.from_template(template)

prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            template="You are a helpful assistant\n"
                     "Answer the following questions as best you can.\n"
                     "You can access to the provided tools.\n"
                     "The value of parameters in tools must be extract from human's message(It can be an empty string, but fabrication is not allowed).\n"
                     ""
        ),
        MessagesPlaceholder(variable_name="chat_history", optional=True),
        HumanMessagePromptTemplate.from_template(template="{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ]
)

# 这是我们的一个有用的辅助类，用于运行工具
# 它接受代理操作并调用该工具，然后返回结果
tool_executor = ToolExecutor(tools_provider.general_tools)


# 定义FC代理节点
def start_function_call_node(data):
    # 构建OpenAI函数代理
    agent_runnable = create_openai_functions_agent(llm, tools_provider.general_tools, prompt)
    # agent_runnable = create_openai_functions_agent(llm, tools_provider.general_tools, chat_prompt)
    # 返回待下一步执行的Function
    function_call_outcome = agent_runnable.invoke(data)
    return {"agent_outcome": function_call_outcome}


# 定义执行工具的函数
def do_execute_tools_node(data) -> Any:
    # 获取最近的代理操作 - 这是在上述`agent`中添加的关键字
    agent_action = data["agent_outcome"]
    # 使用手动加载
    last_message = agent_action.messages[-1]
    tool_name = last_message.additional_kwargs["function_call"]["name"]
    arguments = json.loads(last_message.additional_kwargs["function_call"]["arguments"])
    # if tool_name == "requirement_collect":
    #     arguments["expected_completion_time"] = "5days"
    #     if "return_direct" in arguments:
    #         del arguments["return_direct"]

    agent_action_ = ToolInvocation(
        tool=tool_name,
        tool_input=arguments,
    )
    output = tool_executor.invoke(agent_action_)
    return {"intermediate_steps": [(agent_action, str(output))]}


# 定义将用于确定要继续的条件边的逻辑
def should_continue(data):
    # 如果代理结果是AgentFinish，则返回`exit`字符串
    # 这将在设置图形以定义流程时使用
    steps = data["intermediate_steps"]
    if len(steps) >= 5:
        return "end"
    if isinstance(data["agent_outcome"], AgentFinish):
        return "end"
    # 否则，将返回AgentAction
    # 在这里我们返回`continue`字符串
    # 这将在设置图形以定义流程时使用
    else:
        return "continue"


# 定义流程
workflow = StateGraph(GeneralAgentState)

# 添加节点
workflow.add_node("start_function_call_node", start_function_call_node)
workflow.add_node("do_execute_tools_node", do_execute_tools_node)

# 设置入口
workflow.set_entry_point("start_function_call_node")

# 设置网关
workflow.add_conditional_edges(
    start_key="start_function_call_node",
    # 接下来，我们传入将决定接下来调用哪个节点的函数。
    condition=should_continue,
    # 最后我们传入一个映射。
    # 键是字符串，值是其他节点。
    # END是一个特殊的节点，表示图形应该结束。
    # 将发生的是我们将调用`should_continue`，然后将其输出与此映射中的键进行匹配。
    # 根据匹配结果，然后将调用该节点。
    conditional_edge_mapping={
        # 如果是`tools`，那么我们调用工具节点。
        # "continue": "do_execute_tools_node",
        "continue": "do_execute_tools_node",
        # 否则我们结束。
        "end": END,
    },
)

# 添加连线
workflow.add_edge(start_key="do_execute_tools_node", end_key="start_function_call_node")

# 最后，我们进行编译！
# 这将其编译为LangChain Runnable，
# 这意味着您可以像使用任何其他可运行文件一样使用它
app: CompiledGraph = workflow.compile()
converted_tools_info = tools_provider.converted_tools_info()
print("工具列表：", converted_tools_info)
human_input = "我需要在CREM系统中录入一个用户需求，需求内容是：‘商户后台导航支持二级菜单’。"
# human_input = "马斯克是谁"
# redis_key = "YLL_CHAT_HISTORY"
# cli = RedisClient()
# redis_data: List = cli.get(redis_key)
# if redis_data is None:
#     cli.set(redis_key, [], 30 * 60)
# redis_data = cli.get(redis_key)
redis_data = []
print("历史消息", redis_data)
inputs: Dict = {
    # "tools": converted_tools_info,
    # "tool_names": ["general_query_tool", "requirement_collect_tool"],
    "input": human_input,
    "chat_history": redis_data
}
for s in app.stream(inputs):
    print(list(s.values())[0])
    print("----")
redis_data.append({
    "role": "human",
    "content": human_input
})
# cli.set(redis_key, redis_data, 30 * 60)

# graph = chat_agent_executor.create_tool_calling_executor(llm, tools_provider.general_tools)
# graph.get_graph().print_ascii()
