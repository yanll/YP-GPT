# import os
#
# from langchain.chains import LLMChain
# from langchain_core.prompts import PromptTemplate
# from langchain_openai import AzureChatOpenAI
#
# os.environ["OPENAI_API_VERSION"] = ""
# os.environ["AZURE_OPENAI_ENDPOINT"] = ""
# os.environ["AZURE_OPENAI_API_KEY"] = ""
#
# llm = AzureChatOpenAI(
#     deployment_name="YPgpt"
# )
# prompt = PromptTemplate(
#     template="请问，{country}的首都是哪里 ?",
#     input_variables=["country"],
# )
# chain = LLMChain(llm=llm, prompt=prompt)
# print(chain.invoke("中国"))
#
# print("\n\n")
