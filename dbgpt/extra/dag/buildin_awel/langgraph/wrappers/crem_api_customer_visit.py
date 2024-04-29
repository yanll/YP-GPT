import requests

from dbgpt.extra.dag.buildin_awel.langgraph.wrappers.crem_api_wrapper import getssotoken
from dbgpt.util import envutils


#

def add_customer_visit_record(customer_name, followUpText, followUpTime, followUpTypeName, visitTypeName, contacts):
    url = envutils.getenv("CREM_ENDPOINT") + '/busFollowUp/addCreateFollowUp'

    headers = {
        'yuiassotoken': getssotoken(),
        'Content-Type': 'application/json'
    }

    data = {
        "customerName": customer_name,
        "customerNo": "KA2024-A04260006",
        "followUpText": followUpText,
        "followUpTime": followUpTime,
        "followUpTypeName": followUpTypeName,
        "visitTypeName": "",
        "type": 1,
        "headEntityKey": "followUpInfo",
        "contactIdList": ["0a527c79f2ad770f1b880b8209b2223f"],
        "contacts": contacts
    }

    response = requests.post(url, headers=headers, json=data)

    return response.text
