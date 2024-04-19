from typing import TypedDict, Union, Annotated

from langchain import hub
from langchain.agents import create_openai_functions_agent
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.messages import BaseMessage
from langchain_openai.chat_models import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.graph import END, StateGraph
from langgraph.prebuilt import ToolExecutor
import operator
import os
from dbgpt.util.azure_util import create_azure_llm
from langgraph.prebuilt import chat_agent_executor

os.environ["TAVILY_API_KEY"] = "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"

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "ls__19718564013e408d8d5ae23ad8dbdf29"



tools = [TavilySearchResults(max_results=5)]

# 获取要使用的提示 - 您可以修改此内容！
prompt = hub.pull("hwchase17/openai-functions-agent")


print("提示模版：", prompt)

# 选择将驱动代理的LLM
llm = create_azure_llm()

# 构建OpenAI函数代理
agent_runnable = create_openai_functions_agent(llm, tools, prompt)



class AgentState(TypedDict):
    # 输入字符串
    input: str
    # 会话中以前的消息列表
    chat_history: list[BaseMessage]
    # 给定对代理的调用的结果
    # 需要将`None`作为有效类型，因为这将作为初始值
    agent_outcome: Union[AgentAction, AgentFinish, None]
    # 操作和相应观察结果的列表
    # 在此处我们使用`operator.add`进行注释，以指示对此状态的操作应该被添加到现有值中（而不是覆盖它）
    intermediate_steps: Annotated[list[tuple[AgentAction, str]], operator.add]



# 这是我们的一个有用的辅助类，用于运行工具
# 它接受代理操作并调用该工具，然后返回结果
tool_executor = ToolExecutor(tools)


# 定义代理
def run_agent(data):
    agent_outcome = agent_runnable.invoke(data)
    return {"agent_outcome": agent_outcome}

# Define the function to execute tools
# Define the function to execute tools
def execute_tools(data):
    # Get the most recent agent_outcome - this is the key added in the `agent` above
    agent_action = data["agent_outcome"]
    # response = input(prompt=f"[y/n] continue with: {agent_action}?")
    # if response == "n":
    #     raise ValueError
    output = tool_executor.invoke(agent_action)
    return {"intermediate_steps": [(agent_action, str(output))]}



# Define logic that will be used to determine which conditional edge to go down
def should_continue(data):
    # If the agent outcome is an AgentFinish, then we return `exit` string
    # This will be used when setting up the graph to define the flow
    if isinstance(data["agent_outcome"], AgentFinish):
        return "end"
    # Otherwise, an AgentAction is returned
    # Here we return `continue` string
    # This will be used when setting up the graph to define the flow
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

# We now add a conditional edge
workflow.add_conditional_edges(
    # First, we define the start node. We use `agent`.
    # This means these are the edges taken after the `agent` node is called.
    "agent",
    # Next, we pass in the function that will determine which node is called next.
    should_continue,
    # Finally we pass in a mapping.
    # The keys are strings, and the values are other nodes.
    # END is a special node marking that the graph should finish.
    # What will happen is we will call `should_continue`, and then the output of that
    # will be matched against the keys in this mapping.
    # Based on which one it matches, that node will then be called.
    {
        # If `tools`, then we call the tool node.
        "continue": "action",
        # Otherwise we finish.
        "end": END,
    },
)


# We now add a normal edge from `tools` to `agent`.
# This means that after `tools` is called, `agent` node is called next.
workflow.add_edge("action", "agent")

# Finally, we compile it!
# This compiles it into a LangChain Runnable,
# meaning you can use it as you would any other runnable
app = workflow.compile()

inputs = {"input": "武汉近7天的天气", "chat_history": []}
for s in app.stream(inputs):
    print(list(s.values())[0])
    print("----")




app = chat_agent_executor.create_function_calling_executor(llm, tools)
app.get_graph().print_ascii()