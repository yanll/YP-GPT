import requests

from dbgpt.extra.dag.buildin_awel.langgraph.wrappers.crem_api_wrapper import getssotoken
from dbgpt.util import envutils


#

def add_customer_visit_record(customer_name, followUpText, followUpTime, followUpTypeName, visitTypeName, contacts):
    url = envutils.getenv("CREM_ENDPOINT") + '/busFollowUp/addCreateFollowUp'

    headers = {
        'yuiassotoken': getssotoken(),
        'Content-Type': 'application/json',
        'Cookie': 'JSESSIONID=2F457B72BE5AF9189C4492286D407C20'
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


if __name__ == "__main__":
    # 从外部传入参数调用函数
    customerName = "张华雪报单客户测试"
    followUpText = "测试24"
    followUpTime = "2024-04-26 14:36:57"
    followUpTypeName = "在外约谈"
    visitTypeName = "签约后日常拜访"
    contacts = "张先生"

    response_text = add_customer_visit_record(customerName, followUpText, followUpTime, followUpTypeName, visitTypeName,
                                              contacts)
    print(response_text)
