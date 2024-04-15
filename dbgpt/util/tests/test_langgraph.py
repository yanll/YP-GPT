import os

from langchain_core.messages import HumanMessage
from langchain_openai import AzureChatOpenAI
from langgraph.graph import END, MessageGraph

from dbgpt.util.azure_util import create_azure_llm



def test_graph():
    llm = create_azure_llm()

    graph = MessageGraph()

    graph.add_node("oracle", llm)
    graph.add_edge("oracle", END)

    graph.set_entry_point("oracle")

    runnable = graph.compile()

    rs = runnable.invoke(HumanMessage("What is 1 + 1?"))
    print("\n", rs)
    assert True
