import requests

from dbgpt.util import envutils, consts
from dbgpt.util.lark import ssoutil


#

def add_customer_visit_record(open_id,
                              customer_name,
                              followUpText,
                              followUpTime,
                              followUpTypeName,
                              visitTypeName,
                              contacts):
    url = envutils.getenv("CREM_ENDPOINT") + '/busFollowUp/addCreateFollowUp'

    headers = {
        'yuiassotoken': ssoutil.get_sso_credential(open_id=open_id),
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

    response = requests.post(url, headers=headers, json=data, timeout=consts.request_time_out)

    return response.text
