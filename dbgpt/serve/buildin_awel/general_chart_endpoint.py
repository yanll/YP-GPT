import os
from typing import Dict

from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import AzureChatOpenAI

from dbgpt.core.awel import DAG, HttpTrigger, MapOperator
from langchain_core.messages import HumanMessage
from langchain_openai import AzureChatOpenAI
from langgraph.graph import END, MessageGraph
from dbgpt.util.azure_util import create_azure_llm


class RequestHandleOperator(MapOperator[Dict, str]):
    llm = None

    def __init__(self, **kwargs):
        self.llm = create_azure_llm()
        super().__init__(**kwargs)

    async def map(self, input_body: Dict) -> str:
        print(f"Receive input body: {input_body}")

        prompt = PromptTemplate(
            template="{msg}",
            input_variables=["msg"]
        )
        # chain = LLMChain(llm=self.llm, prompt=prompt)
        # return chain.invoke({"msg": "hello, who are you?"})

        graph = MessageGraph()

        graph.add_node("oracle", self.llm)
        graph.add_edge("oracle", END)

        graph.set_entry_point("oracle")

        runnable = graph.compile()

        rs = runnable.invoke(HumanMessage("What is 1 + 1?"))
        return rs


with DAG("dbgpt_awel_general_chat_endpoint") as dag:
    trigger = HttpTrigger(
        endpoint="/general_chat_endpoint",
        methods="GET",
        request_body=Dict
    )
    map_node = RequestHandleOperator()
    trigger >> map_node
