from flask import Flask, jsonify

from dbgpt.extra.dag.buildin_awel.lark import card_templates
from dbgpt.util.lark import lark_message_util
import requests
from dbgpt.extra.dag.buildin_awel.langgraph.wrappers.lark_event_handler_wrapper import LarkEventHandlerWrapper
from dbgpt.extra.dag.buildin_awel.lark import card_templates
from dbgpt.extra.dag.buildin_awel.monitor import monitor
from dbgpt.util.lark import lark_message_util
import requests
import schedule
import time


from flask import Flask, jsonify
from dbgpt.extra.dag.buildin_awel.lark import card_templates
from dbgpt.extra.dag.buildin_awel.monitor import monitor
from dbgpt.util.lark import lark_message_util

app = Flask(__name__)

def monitor_four():
    hv_data = monitor.main4()
    print("数值的返回结果", hv_data)
    data = hv_data

    name_to_conv_id = {
        '张涛': 'ou_9d42bb88ec8940baf3ad183755131881',
        '段超': 'ou_9d42bb88ec8940baf3ad183755131881',
    }

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
        conv_id = name_to_conv_id.get(name)
        if conv_id:
            content = card_templates.travel_report_content4(
                template_variable={
                    "unlike_callback_event": {
                        "event_type": "unlike",
                        "event_source": "",
                        "event_data": {
                            "message": "航旅波动检测归因"
                        }
                    },
                    "travel_report_list": reports,
                    "title": title,
                    "name": name
                }
            )
            print("Sending to:", name, "Conv ID:", conv_id)
            print("Generated Content:", content)
            resp = lark_message_util.send_card_message(
                receive_id=conv_id,
                content=content
            )
            print("发送的卡片信息是：", resp)
            lark_message_id = resp.get("message_id", "")
            print("lark_message_id是：", lark_message_id)

    return "Success"

@app.route('/monitor_four', methods=['GET'])
def trigger_monitor_four():
    result = monitor_four()
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5670)



