import logging
import uuid
from datetime import datetime

from flask import Flask, jsonify

from dbgpt.extra.dag.buildin_awel.app.service import AppChatService
from dbgpt.extra.dag.buildin_awel.hanglv import hanglv_api_use
from dbgpt.extra.dag.buildin_awel.hanglv.airline_monitor_push import AirlineMonitorPush
from dbgpt.extra.dag.buildin_awel.lark import card_templates
from dbgpt.extra.dag.buildin_awel.monitor import monitor, monitor1bypayer, monitor1bystat
from dbgpt.extra.dag.buildin_awel.monitor.monitor1bystat import Monitor1ByStat
from dbgpt.util.lark import lark_message_util



class AirlineMonitorPush1_1(AirlineMonitorPush):

    def __init__(self):
        self.monitor = Monitor1ByStat()
        super().__init__()

    def store_his_message(self,app_chat_service, sender_open_id, sales, title, content, reason, display_type):
        current_date = datetime.now().strftime('%Y-%m-%d')
        rec = {
            "id": str(uuid.uuid1()),
            "agent_name": "SalesAssistant",
            "node_name": "final",
            "conv_uid": sender_open_id,
            "message_type": "view",
            "content": content,
            "message_detail": "",
            "display_type": display_type,
            "biz_date": current_date,
            "sales": sales,
            "title": title,
            "scene": "",
            "chanel": "",
            "product": "",
            "merchant_no": "",
            "reason": reason,
            "type": "退款笔数波动异常",
            "created_time": "",
            "modified_time": "",
        }
        print("rec的值是：", rec)
        try:
            app_chat_service.add_app_hanglv_msg(rec)
        except Exception as e:
            logging.error(f"Error storing message: {e}")

    def run_push(self):
        hv_data = self.monitor.run()
        print("数值的返回结果", hv_data)
        data = hv_data

        app_chat_service = AppChatService()  # Create the instance once

        # 逐条处理数据并传入 rec
        for item in data:
            # 获取用户 ID
            name = item['name']
            print(name)
            get_sender_open_id = hanglv_api_use.get_user_open_id(name)
            sender_open_id = next(iter(get_sender_open_id.values()), 'noname')
            print(sender_open_id)

            # 合并 reason 字段
            reason = f"{item['reason1']}\n{item['reason2']}\n{item['reason3']}"

            # 构建内容字符串
            content = (
                f"Name: {item['name']}\n"
                f"Title: {item['title']}\n"
                f"Content: {item['content']}\n"
                f"Customer_name: {reason}\n"
            )

            # 调用存储消息的函数
            self.store_his_message(
                app_chat_service,
                sender_open_id=sender_open_id,
                sales=item['name'],
                title=item['title'],
                content=content,
                reason=reason,
                display_type="hanglv_card",
            )

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
            conv_id_map = hanglv_api_use.get_user_open_id(name="张华雪")
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

#
# def store_his_message(app_chat_service, sender_open_id, sales, title, content,  reason, display_type):
#     current_date = datetime.now().strftime('%Y-%m-%d')
#     rec = {
#         "id": str(uuid.uuid1()),
#         "agent_name": "SalesAssistant",
#         "node_name": "final",
#         "conv_uid": sender_open_id,
#         "message_type": "view",
#         "content": content,
#         "message_detail": "",
#         "display_type": display_type,
#         "biz_date": current_date,
#         "sales": sales,
#         "title": title,
#         "scene": "",
#         "chanel": "",
#         "product": "",
#         "merchant_no": "",
#         "reason": reason,
#         "type": "退款笔数波动异常",
#         "created_time": "",
#         "modified_time": "",
#     }
#     print("rec的值是：", rec)
#     try:
#         app_chat_service.add_app_hanglv_msg(rec)
#     except Exception as e:
#         logging.error(f"Error storing message: {e}")
#
# def monitor_one():
#     # first = monitor1bystat.Monitor1ByStat()
#     # hv_data = first.run()
#     # print("数值的返回结果", hv_data)
#     # data = hv_data
#
#     data = [{'title': '交易笔数波动异常', 'name': '张涛',
#              'content': '商户签约名:HX，昨日交易金额0.07万元，环比上升<text_tag color=green >47.37%</text_tag>（商户交易笔数环比）',
#              'reason1': '归因一:商户签约名:HX,商户编号:10001203022,原始场昨日交易金额180.39万元，环比下降<text_tag color=red >-96.85%</text_tag>\n'
#                         '归因一:商户签约名:HX,商户编号:10011975901,原始场昨日交易金额30.30万元，环比下降<text_tag color=red >-91.88%</text_tag>\n'
#                         '归因一:商户签约名:HX,商户编号:10012410483,原始场昨日交易金额10.00万元，环比下降<text_tag color=red >-98.45%</text_tag>',
#              'reason2': '归因二:商户签约名:HX,商户编号:10001203022,原始场景:航司南区,产品:网银，昨日交易金额0.00万元，环比下降<text_tag color=  red  >100.00%</text_tag>\n'
#                         '归因二:商户签约名:HX,商户编号:10011975901,原始场景:航司南区,产品:充值，昨日交易金额27.46万元，环比上升<text_tag color= green >20330.95%</text_tag>\n'
#                         '归因二:商户签约名:HX,商户编号:10011975901,原始场景:航司南区,产品:会员，昨日交易金额2.84万元，环比下降<text_tag color=  red  >84.99%</text_tag>\n'
#                         '归因二:商户签约名:HX,商户编号:10012410483,原始场景:航司南区,产品:充值，昨日交易金额10.00万元，环比下降<text_tag color=  red  >77.96%</text_tag>',
#              'reason3': '归因三:主要影响的付款方签约名:北京美程旅行社有限公司，昨日交易金额2.84万元，环比下降<text_tag color=red>0.85%</text_tag>'}]
#     app_chat_service = AppChatService()  # Create the instance once
#
#     # 逐条处理数据并传入 rec
#     for item in data:
#         # 获取用户 ID
#         name = item['name']
#         print(name)
#         get_sender_open_id = hanglv_api_use.get_user_open_id(name)
#         sender_open_id = next(iter(get_sender_open_id.values()), 'noname')
#         print(sender_open_id)
#
#         # 合并 reason 字段
#         reason = f"{item['reason1']}\n{item['reason2']}\n{item['reason3']}"
#
#         # 构建内容字符串
#         content = (
#             f"Name: {item['name']}\n"
#             f"Title: {item['title']}\n"
#             f"Content: {item['content']}\n"
#             f"Customer_name: {reason}\n"
#         )
#
#         # 调用存储消息的函数
#         store_his_message(
#             app_chat_service,
#             sender_open_id=sender_open_id,
#             sales=item['name'],
#             title=item['title'],
#             content=content,
#             reason=reason,
#             display_type="hanglv_card",
#         )
#
#     name_to_data = {}
#     for report in data:
#         name = report['name']
#         title = report['title']
#         if name not in name_to_data:
#             name_to_data[name] = []
#         report_with_num = report.copy()
#         report_with_num['num'] = len(name_to_data[name]) + 1
#         name_to_data[name].append(report_with_num)
#
#     for name, reports in name_to_data.items():
#         conv_id_map = hanglv_api_use.get_user_open_id(name = "张华雪")
#         for email, conv_id in conv_id_map.items():
#             content = card_templates.travel_report_content1(
#                 template_variable={
#                     "unlike_callback_event": {
#                         "event_type": "unlike",
#                         "event_source": "",
#                         "event_data": {
#                             "message": "航旅波动检测归因1.1"
#                         }
#                     },
#                     "travel_report_list": reports,
#                     "title": title,
#                     "name": name
#                 }
#             )
#             print("发送给:", name, "Conv ID:", conv_id)
#             print("生成的内容:", content)
#             resp = lark_message_util.send_card_message(
#                 receive_id=conv_id,
#                 content=content
#             )
#             print("发送的卡片信息:", resp)
#             lark_message_id = resp.get("message_id", "")
#             print("lark_message_id:", lark_message_id)
#
#     return "Success"

# if __name__ == "__main__":
#     a = AirlineMonitorPush1_1()
#     b = a.run_push()
#     print(b)