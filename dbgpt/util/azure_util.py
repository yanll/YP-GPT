from langchain_openai import AzureChatOpenAI
import os


def create_azure_llm():
    os.environ["OPENAI_API_VERSION"] = os.getenv("PROXY_API_VERSION")
    os.environ["AZURE_OPENAI_ENDPOINT"] = os.getenv("AZURE_OPENAI_ENDPOINT")
    os.environ["AZURE_OPENAI_API_KEY"] = os.getenv("AZURE_OPENAI_KEY")

    llm = AzureChatOpenAI(
        deployment_name=os.getenv("API_AZURE_DEPLOYMENT")
    )
    return llm
