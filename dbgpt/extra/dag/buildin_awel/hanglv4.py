from dbgpt.extra.dag.buildin_awel import hanglv_api_use
from flask import Flask, jsonify
from dbgpt.extra.dag.buildin_awel.lark import card_templates
from dbgpt.util.lark import lark_message_util

app = Flask(__name__)

def monitor_four():
    # hv_data = monitor.main4()
    # print("数值的返回结果", hv_data)
    # data = hv_data
    data = [{'name': '张华雪', 'title': '深航/国航充值业务', 'content': '付方名称:苏州市华谊商务有限公司，航司:ZH——商编:10012407595+场景字段:渠道，近7天充值金额，环比上周上升2520.01%，低于大盘0.61%', 'payer_customer_signedname': '苏州市华谊商务有限公司', 'stat_dispaysignedname': 'ZH', 'customer_no': '10012407595', 'payer_business_scene': '渠道', 'sub_content_rich': '波动详情：  近7天充值金额，环比上周上升<text_tag color=green>2520.01%</text_tag>，低于大盘<text_tag color=red>0.61%</text_tag>'},
        {'name': '张华雪', 'title': '深航/国航充值业务', 'content': '付方名称:杭州泛美航空国际旅行社有限公司，航司:CA——商编:10034228238+场景字段:渠道，近7天充值金额，环比上周上升43.64%，低于大盘0.61%', 'payer_customer_signedname': '杭州泛美航空国际旅行社有限公司', 'stat_dispaysignedname': 'CA', 'customer_no': '10034228238', 'payer_business_scene': '渠道', 'sub_content_rich': '波动详情：  近7天充值金额，环比上周上升<text_tag color=green>43.64%</text_tag>，低于大盘<text_tag color=red>0.61%</text_tag>'},
                {'name': '张华雪', 'title': '深航/国航充值业务', 'content': '付方名称:上海广发航空票务服务有限公司，航司:CA——商编:10034228238+场景字段:渠道，近7天充值金额，环比上周上升40.91%，低于大盘0.61%', 'payer_customer_signedname': '上海广发航空票务服务有限公司', 'stat_dispaysignedname': 'CA', 'customer_no': '10034228238', 'payer_business_scene': '渠道', 'sub_content_rich': '波动详情：  近7天充值金额，环比上周上升<text_tag color=green>40.91%</text_tag>，低于大盘<text_tag color=red>0.61%</text_tag>'},
                {'name': '张华雪', 'title': '深航/国航充值业务', 'content': '付方名称:四川铁航航空运输有限公司，航司:CA——商编:10034228238+场景字段:渠道，近7天充值金额，环比上周下降70.82%，低于大盘0.61%', 'payer_customer_signedname': '四川铁航航空运输有限公司', 'stat_dispaysignedname': 'CA', 'customer_no': '10034228238', 'payer_business_scene': '渠道', 'sub_content_rich': '波动详情：  近7天充值金额，环比上周下降<text_tag color=red>70.82%</text_tag>，低于大盘<text_tag color=red>0.61%</text_tag>'},
    ]

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
        conv_id_map = hanglv_api_use.get_user_open_id(name)
        for email, conv_id in conv_id_map.items():
            content = card_templates.travel_report_content4(
                template_variable={
                    "unlike_callback_event": {
                        "event_type": "unlike",
                        "event_source": "",
                        "event_data": {
                            "message": "航旅波动检测归因4"
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

# @app.route('/monitor_four', methods=['GET'])
# def trigger_monitor_four():
#     result = monitor_four()
#     return jsonify({"result": result})
#
# if __name__ == '__main__':
#     app.run(debug=True, host='127.0.0.1', port=5670)



# 调用函数
#monitor_four()


