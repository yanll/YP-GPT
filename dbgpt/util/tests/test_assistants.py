import requests
import json
import jwt

from dbgpt.extra.dag.buildin_awel.langgraph.assistants.sales_assistant import SalesAssistant
from dbgpt.util import consts


def test_assistants():
    human_input = "吐槽"
    assistant = SalesAssistant()
    rs = assistant._run(input=human_input, conv_uid="123456")
    print(rs)
    assert True
