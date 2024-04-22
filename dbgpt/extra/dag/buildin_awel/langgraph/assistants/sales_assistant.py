import json
import os
import uuid
from typing import Any, Dict

from langchain.agents import create_openai_functions_agent
from langchain_core.agents import AgentFinish
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, SystemMessagePromptTemplate, \
    HumanMessagePromptTemplate
from langgraph.graph import END, StateGraph
from langgraph.graph.graph import CompiledGraph
from langgraph.prebuilt import ToolExecutor, chat_agent_executor

from dbgpt.extra.dag.buildin_awel.app.service import AppChatService, GptsAppService
from dbgpt.extra.dag.buildin_awel.langgraph.assistants.agent_states import GeneralAgentState
from dbgpt.extra.dag.buildin_awel.langgraph.tools.tools_provider import ToolsProvider
from dbgpt.util.azure_util import create_azure_llm

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "ls__19718564013e408d8d5ae23ad8dbdf29"


class SalesAssistant:
    gpts_app_service = None
    app_chat_service = None
    llm = None
    tools_provider = None
    tool_executor = None
    app = None

    def __init__(self, **kwargs):
        self.gpts_app_service = GptsAppService()
        self.app_chat_service = AppChatService()
        self.llm = create_azure_llm()
        self.tools_provider = ToolsProvider()
        self.tool_executor = ToolExecutor(self.tools_provider.general_tools)
        self.app = self.init_flow()
        super().__init__(**kwargs)

    def create_function_call_node(self):
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(
                    template="You are a helpful "
                             "\n"
                             "Answer the following questions as best you can.\n"
                             "You can access to the provided tools.\n"
                             "The value of parameters in tools must be extract from human's message, It can be an empty string, but fabrication is not allowed.\n"
                             ""
                ),
                SystemMessagePromptTemplate.from_template(
                    template="conv_uid=\"{conv_uid}\""
                ),
                MessagesPlaceholder(variable_name="chat_history", optional=True),
                HumanMessagePromptTemplate.from_template(template="{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )

        # 定义FC代理节点，返回：Function/ActionFinish
        def start_function_call_node(data):
            # 构建OpenAI函数代理
            agent_runnable = create_openai_functions_agent(self.llm, self.tools_provider.general_tools, prompt)
            # 返回待下一步执行的Function
            function_call_outcome = agent_runnable.invoke(data)
            print("======== start_function_call_node：", function_call_outcome)
            content = ""
            message_detail = function_call_outcome.json()
            message_type = ""
            if (isinstance(function_call_outcome, AgentFinish)):
                rs = function_call_outcome.return_values
                message_type = "ai"
                content = rs['output']
            else:
                message_type = "assistant"
            rec = {
                "id": str(uuid.uuid1()),
                "agent_name": "SalesAssistant",
                "node_name": "start_function_call_node",
                "conv_uid": data['conv_uid'],
                "message_type": message_type,
                "content": content,
                "message_detail": message_detail
            }
            self.app_chat_service.add_app_chat_his_message(rec)
            return {"agent_outcome": function_call_outcome}

        return start_function_call_node

    def create_do_execute_tools_node(self):
        # 定义执行工具的函数
        def do_execute_tools_node(data) -> Any:
            # 获取最近的代理操作 - 这是在上述`agent`中添加的关键字
            agent_action = data["agent_outcome"]
            # 使用手动加载
            last_message = agent_action.messages[-1]
            tool_name = last_message.additional_kwargs["function_call"]["name"]
            arguments = json.loads(last_message.additional_kwargs["function_call"]["arguments"])
            # if tool_name == "requirement_collect":
            #     arguments["expected_completion_time"] = ""
            #     if "return_direct" in arguments:
            #         del arguments["return_direct"]

            # agent_action_ = ToolInvocation(
            #     tool=tool_name,
            #     tool_input=arguments
            # )
            output = self.tool_executor.invoke(agent_action)

            # function_message = FunctionMessage(content=str(output), name=agent_action_.tool)
            print("======== do_execute_tools_node：", output)
            content = ""
            message_detail = str(output)
            message_type = ""
            if (isinstance(output, AgentFinish)):
                rs = output.return_values
                message_type = "ai"
                content = rs['output']
            else:
                message_type = "assistant"
            rec = {
                "id": str(uuid.uuid1()),
                "agent_name": "SalesAssistant",
                "node_name": "do_execute_tools_node",
                "conv_uid": data['conv_uid'],
                "message_type": message_type,
                "content": content,
                "message_detail": message_detail
            }
            self.app_chat_service.add_app_chat_his_message(rec)

            return {"intermediate_steps": [(agent_action, str(output))]}

        return do_execute_tools_node

    def init_flow(self):
        # 开始节点，解析是否执行工具
        start_function_call_node = self.create_function_call_node()
        # 工具执行节点
        do_execute_tools_node = self.create_do_execute_tools_node()

        # 定义将用于确定要继续的条件边的逻辑
        def should_continue(data):
            # 如果代理结果是AgentFinish，则返回`exit`字符串
            # 这将在设置图形以定义流程时使用
            steps = data["intermediate_steps"]
            if len(steps) >= 2:
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

        # 设置入口节点
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
                "continue": "do_execute_tools_node",
                # 否则我们结束。
                "end": END,
            },
        )
        # 添加连线
        workflow.add_edge(start_key="do_execute_tools_node", end_key="start_function_call_node")
        app: CompiledGraph = workflow.compile()
        return app

    def _run(
            self,
            input: str,
            conv_uid: str = ""
    ) -> Any:
        """Use the tool."""
        print("开始运行销售助理：")
        rec = {
            "id": str(uuid.uuid1()),
            "agent_name": "SalesAssistant",
            "node_name": "",
            "conv_uid": conv_uid,
            "message_type": "human",
            "content": input,
            "message_detail": ""
        }
        self.app_chat_service.add_app_chat_his_message(rec)
        try:
            converted_tools_info = self.tools_provider.converted_tools_info()
            print("工具列表：", converted_tools_info)
            his = self.app_chat_service.get_app_chat_his_messages()
            print("历史消息", his)
            inputs: Dict = {
                "input": input,
                "chat_history": his,
                "conv_uid": conv_uid
            }
            rs = ""
            for s in self.app.stream(inputs):
                row = list(s.values())[0]
                # print("\n---- ", row)
                rs = row
            # s = app.invoke(inputs)
            return rs
        except Exception as e:
            return repr(e)

    def printgraph(self):
        graph = chat_agent_executor.create_tool_calling_executor(self.llm, self.tools_provider.general_tools)
        graph.get_graph().print_ascii()

# human_input = "我需要在CREM系统中录入一个用户需求，需求内容是：‘商户后台导航支持二级菜单’，非常紧急，希望3天完成。"
# assistant = SalesAssistant()
# rs = assistant._run(input=human_input, conv_uid="123456")
# print(rs)
