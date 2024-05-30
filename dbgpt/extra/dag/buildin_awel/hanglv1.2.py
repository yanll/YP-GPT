from dbgpt.extra.dag.buildin_awel import hanglv_api_use
from flask import Flask, jsonify
from dbgpt.extra.dag.buildin_awel.lark import card_templates
from dbgpt.extra.dag.buildin_awel.monitor import monitor, monitor1bypayer
from dbgpt.util.lark import lark_message_util

app = Flask(__name__)

def monitor_one2():
    first = monitor1bypayer.Monitor1ByPayer()
    hv_data = first.run()
    print("数值的返回结果", hv_data)
    data = hv_data
    # data = [
    # {
    #     "title": "交易笔数波动异常",
    #     "name": "张华雪",
    #     "content": "商户签约名:JD，昨日交易金额0.32万元，环比下降-41.52%（商户交易笔数环比）",
    #     "reason4": "该归因暂无",
    #     "reason5": "商户签约名:JD,商户编号:10001004838,原始场景:航司北区,产品:网银，昨日交易金额7.79万元，环比上升2.86%\n",
    #     "reason_3": ""
    # },
    # {
    #     "title": "交易笔数波动异常",
    #     "name": "张华雪",
    #     "content": "商户签约名:UQ，昨日交易金额0.02万元，环比上升440.09%（商户交易笔数环比）",
    #     "reason4": "该归因暂无",
    #     "reason5": "",
    #     "reason_3": ""
    # }]



    name_to_data = {}
    for report in data:
        name = report['name']
        title = report['title']
        if name not in name_to_data:
            name_to_data[name] = []
        report_with_num = report.copy()
        report_with_num['num'] = len(name_to_data[name]) + 1
        name_to_data[name].append(report_with_num)

    for name, reports in name_to_data.items():
        conv_id_map = hanglv_api_use.get_user_open_id(name = "张华雪")
        for email, conv_id in conv_id_map.items():
            content = card_templates.travel_report_content1_2(
                template_variable={
                    "unlike_callback_event": {
                        "event_type": "unlike",
                        "event_source": "",
                        "event_data": {
                            "message": "航旅波动检测归因1.2"
                        }
                    },
                    "travel_report_list": reports,
                    "title": title,
                    "name": name
                }
            )
            print("发送给:", name, "Conv ID:", conv_id)
            print("生成的内容:", content)
            resp = lark_message_util.send_card_message(
                receive_id=conv_id,
                content=content
            )
            print("发送的卡片信息:", resp)
            lark_message_id = resp.get("message_id", "")
            print("lark_message_id:", lark_message_id)

    return "Success"



# 调用函数
monitor_one2()


