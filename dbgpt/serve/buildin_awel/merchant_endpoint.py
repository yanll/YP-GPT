import os
from typing import Optional, List
import requests
import json
from langchain.agents.chat.base import ChatAgent

from langchain.agents import AgentType, initialize_agent, AgentExecutor
from langchain.chains.llm import LLMChain
from langchain.tools import BaseTool
from langchain_community.agent_toolkits.base import BaseToolkit
from langchain_community.agent_toolkits.json.base import create_json_agent
from langchain_community.agent_toolkits.json.toolkit import JsonToolkit
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_openai import AzureChatOpenAI
from langchain.agents import create_react_agent
from dbgpt._private.pydantic import BaseModel, Field
from dbgpt.core.awel import DAG, HttpTrigger, MapOperator
from dbgpt.util.dmallutil import DmallClient


class ReqContext(BaseModel):
    conv_uid: str = Field(..., description="会话标识")


class TriggerReqBody(BaseModel):
    message: str = Field(..., description="消息内容")
    context: Optional[ReqContext] = Field(
        default=None, description="The context of the model request."
    )


class RequestHandleOperator(MapOperator[TriggerReqBody, str]):
    llm = None

    def __init__(self, **kwargs):
        os.environ["OPENAI_API_VERSION"] = os.getenv("PROXY_API_VERSION")
        os.environ["AZURE_OPENAI_ENDPOINT"] = os.getenv("AZURE_OPENAI_ENDPOINT")
        os.environ["AZURE_OPENAI_API_KEY"] = os.getenv("AZURE_OPENAI_KEY")

        self.llm = AzureChatOpenAI(
            deployment_name=os.getenv("API_AZURE_DEPLOYMENT")
        )
        super().__init__(**kwargs)

    async def map(self, input_body: TriggerReqBody) -> str:
        print(f"Receive input body: {input_body}")

        tools = [ExtractMerchantNumberTool(), SearchMerchantDetailTool(), SummaryMerchantDetailTool()]

        prompt = PromptTemplate(
            template="{msg}",
            input_variables=["msg"]
        )

        # chain = LLMChain(llm=self.llm, prompt=prompt)
        # airs = chain.invoke(input_body.message)
        # print("调用LLM：", airs)

        # deprecated
        # dagent = initialize_agent(
        #     tools, self.llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
        # )
        # dagent.invoke(input_body.message)

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

        # chat_prompt = ChatPromptTemplate.from_messages([
        #     ("system", "你是一个内容专家，请提取出我输入信息中的商户编号。"),
        #     ("human", "{user_input}"),
        # ])
        react_agent = create_react_agent(
            tools=tools,
            llm=self.llm,
            prompt=chat_prompt
        )
        agent_executor = AgentExecutor(agent=react_agent, tools=tools, verbose=True)

        rs = agent_executor.invoke({
            "input": input_body.message
        })

        out = rs['output']
        if "text" in rs:
            return out['text']
        return out


with DAG("dbgpt_awel_merchant_endpoint") as dag:
    trigger = HttpTrigger(
        endpoint="/merchant_endpoint",
        methods="POST",
        request_body=TriggerReqBody
    )
    map_node = RequestHandleOperator()
    trigger >> map_node


class ExtractMerchantNumberTool(BaseTool):
    name = "ExtractMerchantNumberTool"
    description = "提取商户编号"
    return_direct = False

    def _run(self, msg: str) -> str:


        prompt = PromptTemplate(
            template="从我输入的信息提取出类型是数字的商户编号，然后返回商户编号，不要回复多余内容。以下是我发送的消息：{msg}",
            input_variables=["msg"]
        )

        chain = LLMChain(llm=self.llm, prompt=prompt)
        rs = chain.invoke({"msg": msg})
        print("商编提取结果：", rs)
        return rs


class SearchMerchantDetailTool(BaseTool):
    name = "SearchMerchantDetailTool"
    description = "查询商户详细信息"
    return_direct = False

    def _run(self, merchant_no: str) -> str:
        dmall_client = DmallClient()
        data = dmall_client.post(
            api_name="query_merchant_info",
            parameters={
                "CUSTOMERNUMBER": merchant_no
            }
        )
        return data.json()['data']['data']


class SummaryMerchantDetailTool(BaseTool):
    name = "SummaryMerchantDetailTool"
    description = "总结输出商户信息"
    return_direct = False

    def _run(self, merchant_info: str) -> str:


        prompt = PromptTemplate(
            template="将我输入的信息总结后输出。根据字段总结，不要编造和猜测字段的含义，不要丢失字段信息。以下是我发送的消息：{msg}",
            input_variables=["msg"]
        )

        chain = LLMChain(llm=self.llm, prompt=prompt)
        rs = chain.invoke({"msg": merchant_info})
        print("商户信息总结结果：", rs)
        if "text" in rs:
            return rs['text']
        return rs
