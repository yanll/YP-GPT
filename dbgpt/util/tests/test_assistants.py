import requests
import json
import jwt

from dbgpt.extra.dag.buildin_awel.langgraph.assistants.sales_assistant import SalesAssistant
from dbgpt.util import consts


def test_assistants():
    human_input = "吐槽"
    assistant = SalesAssistant()
    rs = assistant._run(input=human_input, conv_uid="ou_8183ebf29633d5af91fa0b32a0c05bcf")
    print(rs)
    assert True
