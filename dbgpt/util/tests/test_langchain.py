import os

from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import AzureChatOpenAI

from dbgpt.util.azure_util import create_azure_llm


def test_chain():
    llm = create_azure_llm()
    prompt = PromptTemplate(
        template="请问，{country}的首都是哪里 ?",
        input_variables=["country"],
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    print("\n", chain.invoke("中国"))

    print("\n\n")
    assert True
