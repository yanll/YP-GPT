from dbgpt.extra.dag.buildin_awel import hanglv_api_use
from dbgpt.extra.dag.buildin_awel.lark import card_templates
from dbgpt.util.lark import lark_message_util


def monitor_three():
    # hv_data = monitor.main3()
    # print("数值的返回结果", hv_data)
    # data = hv_data

    data = [
  {
    "name": "张华雪",
    "title": "商户（收方或付方）产品波动异常",
    "customer_name": "JD",
    "content_rich": "波动详情：交易无明显波动，但会员产品结构有变化，变化值为<text_tag color=orange>13.66%</text_tag>，请关注。",
    "type": "商户签约名"
  },
  {
    "name": "刘博",
    "title": "商户（收方或付方）产品波动异常",
    "customer_name": "A6",
    "content_rich": "波动详情：交易无明显波动，但旗舰店产品结构有变化，变化值为<text_tag color=orange>-11.25%</text_tag>，请关注。",
    "type": "商户签约名"
  },
  {
    "name": "张华雪",
    "title": "商户（收方或付方）产品波动异常",
    "customer_name": "DZ",
    "content_rich": "波动详情：交易无明显波动，但会员产品结构有变化，变化值为<text_tag color=orange>12.94%</text_tag>，请关注。",
    "type": "商户签约名"
  },
  {
    "name": "张华雪",
    "title": "商户（收方或付方）产品波动异常",
    "customer_name": "MU-2",
    "content_rich": "波动详情：交易无明显波动，但会员产品结构有变化，变化值为<text_tag color=orange>31.87%</text_tag>，请关注。",
    "type": "商户签约名"
  }
]

    # 按名字过滤数据
    name_to_data = {}
    for report in data:
        name = report['name']
        title = report['title']
        if name not in name_to_data:
            name_to_data[name] = []
        report_with_num = report.copy()
        report_with_num['num'] = len(name_to_data[name]) + 1
        name_to_data[name].append(report_with_num)

    # 发送消息
    for name, reports in name_to_data.items():
        conv_id_map = hanglv_api_use.get_user_open_id(name)
        for email, conv_id in conv_id_map.items():
            content = card_templates.travel_report_content3(
                template_variable={
                    "unlike_callback_event": {
                        "event_type": "unlike",
                        "event_source": "",
                        "event_data": {
                            "message": "航旅波动检测归因3"
                        }
                    },
                    "travel_report_list": reports,  # 将所有报告传递给模板
                    "title": reports[0]['title'],  # 使用第一个报告的标题
                    "name": name
                }
            )

            # 添加调试信息，打印生成的内容
            print("Sending to:", name, "Conv ID:", conv_id)
            print("Generated Content:", content)

            resp = lark_message_util.send_card_message(
                receive_id=conv_id,  # 使用 conv_id 作为接收者的 ID
                content=content
            )
            print("发送的卡片信息是：", resp)

            # lark_message_id = resp.get("message_id", "")
            # print("lark_message_id是：", lark_message_id)


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
#monitor_three()