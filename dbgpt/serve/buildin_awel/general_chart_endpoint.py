import os
from typing import Dict

from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import AzureChatOpenAI

from dbgpt.core.awel import DAG, HttpTrigger, MapOperator


class RequestHandleOperator(MapOperator[Dict, str]):
    llm = None

    def __init__(self, **kwargs):
        os.environ["OPENAI_API_VERSION"] = os.getenv("PROXY_API_VERSION")
        os.environ["AZURE_OPENAI_ENDPOINT"] = os.getenv("AZURE_OPENAI_ENDPOINT")
        os.environ["AZURE_OPENAI_API_KEY"] = os.getenv("AZURE_OPENAI_KEY")

        self.llm = AzureChatOpenAI(
            deployment_name=os.getenv("API_AZURE_DEPLOYMENT")
        )

        super().__init__(**kwargs)

    async def map(self, input_body: Dict) -> str:
        print(f"Receive input body: {input_body}")

        prompt = PromptTemplate(
            template="{msg}",
            input_variables=["msg"]
        )
        chain = LLMChain(llm=self.llm, prompt=prompt)
        return chain.invoke({"msg": "hello, who are you?"})


with DAG("dbgpt_awel_general_chat_endpoint") as dag:
    trigger = HttpTrigger(
        endpoint="/general_chat_endpoint",
        methods="GET",
        request_body=Dict
    )
    map_node = RequestHandleOperator()
    trigger >> map_node
