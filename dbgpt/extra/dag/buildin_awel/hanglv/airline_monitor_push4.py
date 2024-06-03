import logging
import uuid
from datetime import datetime

from dbgpt.extra.dag.buildin_awel.app.service import AppChatService
from dbgpt.extra.dag.buildin_awel.hanglv import hanglv_api_use
from dbgpt.extra.dag.buildin_awel.hanglv.airline_monitor_push import AirlineMonitorPush
from dbgpt.extra.dag.buildin_awel.lark import card_templates
from dbgpt.extra.dag.buildin_awel.monitor.monitor4 import Monitor4
from dbgpt.util.lark import lark_message_util


class AirlineMonitorPush4(AirlineMonitorPush):

    def __init__(self):
        self.monitor = Monitor4()
        super().__init__()

    def store_his_message(self, app_chat_service, sales, title, content, product, scene, merchant_no,
                          chanel, display_type):
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
            "scene": scene,
            "chanel": chanel,
            "product": product,
            "merchant_no": merchant_no,
            "reason": "",
            "type": "航旅波动检测归因4_深航/国航充值业务",
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
                f"Payer Customer Signed Name: {item['payer_customer_signedname']}\n"
                f"Stat Display Signed Name: {item['stat_dispaysignedname']}\n"
                f"Customer No: {item['customer_no']}\n"
                f"Payer Business Scene: {item['payer_business_scene']}\n"
                f"Sub Content Rich: {item['sub_content_rich']}\n"
            )

            # 调用存储消息的函数
            self.store_his_message(
                app_chat_service,
                sales=item['name'],
                title=item['title'],
                content=content,
                product=item['payer_customer_signedname'],
                scene=item['stat_dispaysignedname'],
                merchant_no=item['customer_no'],
                chanel=item['payer_business_scene'],
                display_type="hanglv_card"
            )

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

        for name, reports in name_to_data.items():
            if name not in conv_id_cache:
                # 只在第一次遇到该 name 时调用 API
                conv_id_cache[name] = hanglv_api_use.get_user_open_id(name)
            conv_id_map = conv_id_cache[name]
            print("cov_id的合集", conv_id_map)
            conv_id_map = {'huaxue.zhang@yeepay.com': 'ou_9d42bb88ec8940baf3ad183755131881',
                           'liangliang.yan@yeepay.com': 'ou_a22698cffd738d7851ef30f5dad1a06c',
                           'bo.liu-2@yeepay.com': 'ou_850210efe332c6e50256b21b29832f1f',
                           'yangsheng.su@yeepay.com': 'ou_079964d3b15f58fc330058a629b8ed41'}
            for email, conv_id in conv_id_map.items():
                content = card_templates.travel_report_content4(
                    template_variable={
                        "unlike_callback_event": {
                            "event_type": "unlike",
                            "event_source": "",
                            "event_data": {
                                "message": "航旅波动检测归因4_深航/国航充值业务"
                            }
                        },
                        "travel_report_list": reports,
                        "title": title,
                        "name": name
                    }
                )
                print("发送给:", name, "Conv ID:", conv_id)
                print("生成的内容:", content)
                try:
                    resp = lark_message_util.send_card_message(
                        receive_id=conv_id,
                        content=content
                    )
                    print("发送的卡片信息:", resp)
                    lark_message_id = resp.get("message_id", "")
                    print("lark_message_id:", lark_message_id)
                except Exception as e:
                    logging.error(f"Error sending message to {name}: {e}")

        return "Success"
