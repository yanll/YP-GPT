import logging
import uuid
from datetime import datetime

from dbgpt.extra.dag.buildin_awel.app.service import AppChatService
from dbgpt.extra.dag.buildin_awel.hanglv import hanglv_api_use
from dbgpt.extra.dag.buildin_awel.hanglv.airline_monitor_push import AirlineMonitorPush
from dbgpt.extra.dag.buildin_awel.lark import card_templates
from dbgpt.extra.dag.buildin_awel.monitor import monitor, monitor3
from dbgpt.extra.dag.buildin_awel.monitor.monitor3 import Monitor3
from dbgpt.util.lark import lark_message_util

class AirlineMonitorPush3(AirlineMonitorPush):

    def __init__(self):
        self.monitor = Monitor3()
        super().__init__()

    def store_his_message(self,app_chat_service, sales, title, content, merchant_no, product, display_type):
        current_date = datetime.now().strftime('%Y-%m-%d')
        rec = {
            "id": str(uuid.uuid1()),
            "agent_name": "SalesAssistant",
            "node_name": "final",
            "message_type": "view",
            "content": content,
            "message_detail": "",
            "display_type": display_type,
            "biz_date": current_date,
            "sales": sales,
            "title": title,
            "scene": "",
            "chanel": "",
            "product": product,
            "merchant_no": merchant_no,
            "reason": "",
            "type": "航旅波动检测归因3_商户（收方或付方）产品波动异常",
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

            # 构建内容字符串
            content = (
                f"Name: {item['name']}\n"
                f"Title: {item['title']}\n"
                f"Content: {item['content']}\n"
                f"Customer_name: {item['customer_name']}\n"
                f"Type: {item['type']}\n"

            )

            # 调用存储消息的函数
            self.store_his_message(
                app_chat_service,
                sales=item['name'],
                title=item['title'],
                content=content,
                merchant_no=item['customer_name'],
                product=item['type'],
                display_type="hanglv_card",

            )

        # 按名字过滤数据
        name_to_data = {}
        conv_id_cache = {}

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
            if name not in conv_id_cache:
                # 只在第一次遇到该 name 时调用 API
                conv_id_cache[name] = hanglv_api_use.get_user_open_id(name)
            conv_id_map = conv_id_cache[name]
            print("cov_id的合集", conv_id_map)
            for email, conv_id in conv_id_map.items():
                content = card_templates.travel_report_content3(
                    template_variable={
                        "unlike_callback_event": {
                            "event_type": "unlike",
                            "event_source": "",
                            "event_data": {
                                "message": "航旅波动检测归因3_商户（收方或付方）产品波动异常"
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












