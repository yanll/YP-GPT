
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

def monitor_four():
    hv_data = monitor.main()
    print("数值的返回结果", hv_data)
    data = hv_data
    # 原始数据

    # 名字与 conv_id 的对应关系
    name_to_conv_id = {
        '张涛': 'ou_9d42bb88ec8940baf3ad183755131881',
        '段超': 'ou_9d42bb88ec8940baf3ad183755131881'
    }

    # 按名字过滤数据
    name_to_data = {}
    for report in data:
        name = report['name']
        title = report['title']
        if name not in name_to_data:
            name_to_data[name] = []
        report_with_num = report.copy()  # 创建报告的副本，以防止修改原始数据
        report_with_num['num'] = len(name_to_data[name]) + 1  # 添加 num 字段，从 1 开始
        name_to_data[name].append(report_with_num)
    # 发送消息
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
                    "travel_report_list": reports,  # 将所有报告传递给模板
                    "title": title,
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

            lark_message_id = resp.get("message_id", "")
            print("lark_message_id是：", lark_message_id)



# 每隔一段时间调用一次 monitor_four 函数
#schedule.every(10).seconds.do(monitor_four)  # 每10秒执行一次
#schedule.every(30).minutes.do(monitor_four)  # 每隔30分钟调用一次
# schedule.every().hour.do(monitor_four)  # 每隔一小时调用一次
#schedule.every().day.at("15:30").do(monitor_four)  # 每天的10:30调用一次
# 可以根据需求选择不同的调度方式

# while True:
#     schedule.run_pending()
#     time.sleep(1)
# 调用函数
# monitor_four()



