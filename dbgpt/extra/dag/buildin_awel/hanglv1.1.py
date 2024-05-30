from dbgpt.extra.dag.buildin_awel import hanglv_api_use
from flask import Flask, jsonify
from dbgpt.extra.dag.buildin_awel.lark import card_templates
from dbgpt.extra.dag.buildin_awel.monitor import monitor, monitor1bypayer, monitor1bystat
from dbgpt.util.lark import lark_message_util

app = Flask(__name__)

def monitor_one():
    first = monitor1bystat.Monitor1ByStat()
    hv_data = first.run()
    print("数值的返回结果", hv_data)
    data = hv_data

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
            content = card_templates.travel_report_content1(
                template_variable={
                    "unlike_callback_event": {
                        "event_type": "unlike",
                        "event_source": "",
                        "event_data": {
                            "message": "航旅波动检测归因1.1"
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




