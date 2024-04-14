import os

from langchain_core.messages import HumanMessage
from langchain_openai import AzureChatOpenAI
from langgraph.graph import END, MessageGraph




def test_graph():
    os.environ["OPENAI_API_VERSION"] = os.getenv("PROXY_API_VERSION")
    os.environ["AZURE_OPENAI_ENDPOINT"] = os.getenv("AZURE_OPENAI_ENDPOINT")
    os.environ["AZURE_OPENAI_API_KEY"] = os.getenv("AZURE_OPENAI_KEY")

    llm = AzureChatOpenAI(
        deployment_name=os.getenv("API_AZURE_DEPLOYMENT")
    )

    graph = MessageGraph()

    graph.add_node("oracle", llm)
    graph.add_edge("oracle", END)

    graph.set_entry_point("oracle")

    runnable = graph.compile()

    rs = runnable.invoke(HumanMessage("What is 1 + 1?"))
    print("\n", rs)
    assert True
