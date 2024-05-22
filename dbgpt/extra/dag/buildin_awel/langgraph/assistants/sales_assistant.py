import json
import logging
import os
import time
import uuid
from typing import Any, Dict

from langchain.agents import create_openai_functions_agent
from langchain_core.agents import AgentFinish, AgentActionMessageLog
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
    use_storage = True
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
                    template="You are a helpful ai assistant."
                             "\n"
                             "Answer the following questions as best you can and answer in simplified Chinese.\n"
                             "You have access to the provided tools.\n"
                             "The value of parameters in tools must be extract from the following questions, It can be an empty string, but fabrication is not allowed.\n"
                             ""
                ),
                SystemMessagePromptTemplate.from_template(
                    template=""
                             "conv_uid=\"{conv_uid}\"\n"
                             "current_system_time_string=\"{current_system_time_string}\"\n"
                             ""
                ),
                SystemMessagePromptTemplate.from_template(
                    template=""
                             "You can calculate other times based on 'current_system_time_string', such as yesterday、tomorrow or next tuesday and so on.\n"
                             ""
                ),
                SystemMessagePromptTemplate.from_template(
                    template=""
                             "为了更好的回答用户的问题，以下名词可以作为参考：\n"
                             "1、易宝：是一家企业，指“易宝支付有限公司”\n"
                             ""
                ),
                SystemMessagePromptTemplate.from_template(
                    template="请仔细思考并检查回答的内容是否正确，是否符合我的要求。\n"
                             "以下是注意事项：\n"
                             "1、回复内容中如果出现“抱歉”、“很抱歉”、“非常抱歉”之类的词，请改成“好的”。\n"
                             "2、请将回复内容格式化、美化后输出，可以适当换行便于阅读。\n"
                             "3、调用工具时，参数字段的值提取自用户输入，如果提取不到则默认为“”，不要编造生成内容。\n"

                             ""
                ),
                MessagesPlaceholder(variable_name="chat_history", optional=True),
                HumanMessagePromptTemplate.from_template(template="{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad")
            ]
        )

        # 定义FC代理节点，返回：Function/ActionFinish
        def thought_function_call_node(data):
            # 构建OpenAI函数代理
            agent_runnable = create_openai_functions_agent(self.llm, self.tools_provider.general_tools, prompt)
            # 返回待下一步执行的Function
            function_call_outcome = agent_runnable.invoke(data)
            # print("======== thought_function_call_node：", function_call_outcome)
            content = ""
            message_detail = function_call_outcome.json()
            message_type = ""
            if isinstance(function_call_outcome, AgentFinish):
                rs = function_call_outcome.return_values
                message_type = "ai"
                content = rs['output']
            else:
                message_type = "assistant"
            rec = {
                "id": str(uuid.uuid1()),
                "agent_name": "SalesAssistant",
                "node_name": "thought_function_call_node",
                "conv_uid": data['conv_uid'],
                "message_type": message_type,
                "content": content,
                "message_detail": message_detail,
                "display_type": "",
                "lark_message_id": ""
            }
            if self.use_storage is True:
                self.app_chat_service.add_app_chat_his_message(rec)
            last_outcome = ""
            if 'intermediate_steps' not in data:
                return {"agent_outcome": function_call_outcome, "last_outcome": last_outcome}
            intermediate_steps = data['intermediate_steps']
            if len(intermediate_steps) > 0:
                last_step = intermediate_steps[-1]
                if isinstance(last_step, tuple):
                    last_outcome = last_step[-1]
            # 上一步的执行结果继续输出
            if isinstance(function_call_outcome, AgentFinish):
                return_values = function_call_outcome.return_values
                if isinstance(return_values, dict):
                    return_values['last_output'] = last_outcome

            return {"agent_outcome": function_call_outcome, "last_outcome": last_outcome}

        return thought_function_call_node

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
            # print("======== do_execute_tools_node：", output)
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
                "message_detail": message_detail,
                "display_type": "",
                "lark_message_id": ""
            }
            if self.use_storage is True:
                self.app_chat_service.add_app_chat_his_message(rec)

            tool_execute_result = {"intermediate_steps": [(agent_action, str(output))]}
            print("tool_execute_result:", tool_name, tool_execute_result)
            return tool_execute_result

        return do_execute_tools_node

    def create_do_knowledge_tool_node(self):
        # 定义知识库工具的函数
        def do_execute_knowledge_node(data) -> Any:
            agent_outcome = data["agent_outcome"]
            agent_action = AgentActionMessageLog(
                message_log=[],
                log="Invoking: knowledge_tool",
                tool="knowledge_tool",
                tool_input={
                    "conv_id": data["conv_uid"],
                    "question": data["input"],
                    "ref": agent_outcome.log
                }
            )
            output = self.tool_executor.invoke(agent_action)
            tool_execute_result = {"intermediate_steps": [(agent_action, str(output))]}
            print("tool_execute_result:", "knowledge_tool", tool_execute_result)
            return tool_execute_result

        return do_execute_knowledge_node

    def init_flow(self):
        # 开始节点，解析是否执行工具
        thought_function_call_node = self.create_function_call_node()
        # 工具执行节点
        do_execute_tools_node = self.create_do_execute_tools_node()

        # do_execute_knowledge_node = self.create_do_knowledge_tool_node()

        # 定义将用于确定要继续的条件边的逻辑
        def should_continue(data):
            # 如果代理结果是AgentFinish，则返回`exit`字符串
            # 这将在设置图形以定义流程时使用
            steps = data["intermediate_steps"]
            if len(steps) >= 5:
                return "end"
            if isinstance(data["agent_outcome"], AgentFinish):
                agent_outcome: AgentFinish = data["agent_outcome"]
                return_values = agent_outcome.return_values
                last_output = return_values["last_output"]
                # 没有执行过工具
                # if last_output == "":
                #     return "continue_knowledge"
                return "end"
            else:
                return "continue"

        # 定义流程
        workflow = StateGraph(GeneralAgentState)

        # 添加节点
        workflow.add_node("thought_function_call_node", thought_function_call_node)
        workflow.add_node("do_execute_tools_node", do_execute_tools_node)
        # workflow.add_node("do_execute_knowledge_node", do_execute_knowledge_node)

        # 设置入口节点
        workflow.set_entry_point("thought_function_call_node")

        # 设置网关
        workflow.add_conditional_edges(
            source="thought_function_call_node",
            # 接下来，我们传入将决定接下来调用哪个节点的函数。
            path=should_continue,
            # 最后我们传入一个映射。
            # 键是字符串，值是其他节点。
            # END是一个特殊的节点，表示图形应该结束。
            # 将发生的是我们将调用`should_continue`，然后将其输出与此映射中的键进行匹配。
            # 根据匹配结果，然后将调用该节点。
            path_map={
                "continue": "do_execute_tools_node",
                # "continue_knowledge": "do_execute_knowledge_node",
                "end": END,
            }
        )
        # 添加连线
        workflow.add_edge(start_key="do_execute_tools_node", end_key="thought_function_call_node")
        # workflow.add_edge(start_key="do_execute_knowledge_node", end_key="thought_function_call_node")
        app: CompiledGraph = workflow.compile()
        return app

    def _run(
            self,
            input: str,
            conv_uid: str = ""
    ) -> Any:
        """Use the tool."""
        print("开始运行销售助理：")

        try:
            # converted_tools_info = self.tools_provider.converted_tools_info()
            # print("工具列表：", converted_tools_info)
            his = []
            if self.use_storage is True:
                his = self.app_chat_service.get_app_chat_his_messages_by_conv_uid(conv_uid=conv_uid)
            inputs: Dict = {
                "input": input,
                "chat_history": his,
                "conv_uid": conv_uid,
                "current_system_time_string": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            }
            rec = {
                "id": str(uuid.uuid1()),
                "agent_name": "SalesAssistant",
                "node_name": "",
                "conv_uid": conv_uid,
                "message_type": "human",
                "content": input,
                "message_detail": "",
                "display_type": "text",
                "lark_message_id": ""
            }
            # self.app_chat_service.add_app_chat_his_message(rec)
            rs = ""
            print("Execute Agent")
            for s in self.app.stream(inputs):
                row = list(s.values())[0]
                rs = row
            # s = self.app.invoke(inputs)
            return rs
        except Exception as e:
            logging.error("销售助理运行异常：", e)
            raise e

    def printgraph(self):
        graph = chat_agent_executor.create_tool_calling_executor(self.llm, self.tools_provider.general_tools)
        graph.get_graph().print_ascii()

# assistant = SalesAssistant()
# assistant.printgraph()
