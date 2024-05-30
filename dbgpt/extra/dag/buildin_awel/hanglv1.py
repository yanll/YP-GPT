from dbgpt.extra.dag.buildin_awel import hanglv_api_use
from flask import Flask, jsonify
from dbgpt.extra.dag.buildin_awel.lark import card_templates
from dbgpt.extra.dag.buildin_awel.monitor import monitor
from dbgpt.util.lark import lark_message_util

app = Flask(__name__)

def monitor_one():
    # hv1_data = monitor.Monitor1()
    # hv_data = hv1_data.run()
    # print("数值的返回结果", hv_data)
    # data = hv_data
    data = [
    {
        "title": "交易笔数波动异常",
        "name": "张华雪",
        "content": "商户签约名:JD，昨日交易金额0.32万元，环比下降-41.52%（商户交易笔数环比）",
        "reason_1": None,
        "reason_2": "商户签约名:JD,商户编号:10001004838,原始场景:航司北区,产品:网银，昨日交易金额7.79万元，环比上升2.86%\n",
        "reason_3": ""
    },
    {
        "title": "交易笔数波动异常",
        "name": "张华雪",
        "content": "商户签约名:UQ，昨日交易金额0.02万元，环比上升440.09%（商户交易笔数环比）",
        "reason_1": "",
        "reason_2": "",
        "reason_3": ""
    },
    {
        "title": "交易笔数波动异常",
        "name": "张华雪",
        "content": "商户签约名:HX，昨日交易金额0.07万元，环比上升61.26%（商户交易笔数环比）",
        "reason_1": None,
        "reason_2": "商户签约名:HX,商户编号:10011975901,原始场景:航司南区,产品:充值，昨日交易金额0.13万元，环比下降0.99%\n商户签约名:HX,商户编号:10012410483,原始场景:航司南区,产品:充值，昨日交易金额45.37万元，环比上升3.27%\n",
        "reason_3": ""
    },
    {
        "title": "交易笔数波动异常",
        "name": "张华雪",
        "content": "商户签约名:苏南瑞丽航空有限公司，昨日交易金额0.05万元，环比下降-21.84%（商户交易笔数环比）",
        "reason_1": "",
        "reason_2": "",
        "reason_3": "主要影响的付款方签约名:云南中旺国际旅行社有限公司，昨日交易金额12.65万元，环比上升7.27%\n"
    },
    {
        "title": "交易笔数波动异常",
        "name": "张华雪",
        "content": "商户签约名:CZ，昨日交易金额6.33万元，环比上升30.73%（商户交易笔数环比）",
        "reason_1": None,
        "reason_2": "商户签约名:CZ,商户编号:10011443729,原始场景:航司南区,产品:无卡，昨日交易金额3.23万元，环比下降0.56%\n商户签约名:CZ,商户编号:10034305046,原始场景:航司南区,产品:无卡，昨日交易金额1.63万元，环比上升180.83%\n",
        "reason_3": "主要影响的付款方签约名:北京华达国际旅行社有限公司，昨日交易金额55.15万元，环比上升4.42%\n主要影响的付款方签约名:北京金达航空服务有限公司，昨日交易金额10.05万元，环比下降0.55%\n"
    }]



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
            content = card_templates.travel_report_content1(
                template_variable={
                    "unlike_callback_event": {
                        "event_type": "unlike",
                        "event_source": "",
                        "event_data": {
                            "message": "航旅波动检测归因1"
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

# 每隔一段时间调用一次 monitor_four 函数
#schedule.every(60).seconds.do(monitor_two)  # 每10秒执行一次
#schedule.every(30).minutes.do(monitor_two)  # 每隔30分钟调用一次
# schedule.every().hour.do(monitor_two)  # 每隔一小时调用一次
#schedule.every().day.at("15:30").do(monitor_two)  # 每天的10:30调用一次
# 可以根据需求选择不同的调度方式

#while True:
#    schedule.run_pending()
 #   time.sleep(1)

# 调用函数
# monitor_one()


