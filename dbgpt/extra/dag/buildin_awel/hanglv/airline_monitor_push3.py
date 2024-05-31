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

    def store_his_message(self,app_chat_service, sender_open_id, sales, title, content, merchant_no, product, display_type):
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
            "product": product,
            "merchant_no": merchant_no,
            "reason": "",
            "type": "商户（收方或付方）产品波动异常",
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
                sender_open_id=sender_open_id,
                sales=item['name'],
                title=item['title'],
                content=content,
                merchant_no=item['customer_name'],
                product=item['type'],
                display_type="hanglv_card",

            )

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
            conv_id_map = hanglv_api_use.get_user_open_id(name="张华雪")
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











#
# def store_his_message(app_chat_service, sender_open_id, sales, title, content,  merchant_no, product, display_type):
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
#         "product": product,
#         "merchant_no": merchant_no,
#         "reason": "",
#         "type": "商户（收方或付方）产品波动异常",
#         "created_time": "",
#         "modified_time": "",
#     }
#     print("rec的值是：", rec)
#     try:
#         app_chat_service.add_app_hanglv_msg(rec)
#     except Exception as e:
#         logging.error(f"Error storing message: {e}")
# def monitor_three():
#
#     # first = monitor3.Monitor3()
#     # hv_data = first.run()
#     # print("数值的返回结果", hv_data)
#     # data = hv_data
#     data = [{'name': '张涛', 'title': '商户（收方或付方）产品波动异常', 'customer_name': 'HU', 'content': '交易无明显波动，但会员产品结构有变化，变化值为345.88%，请关注。', 'content_rich': '波动详情：      交易无明显波动，但会员产品结构有变化，变化值为<text_tag color=carmine>345.88%</text_tag>，请关注。', 'type': '商户签约名'}, {'name': '张涛', 'title': '商户（收方或付方）产品波动异常', 'customer_name': 'HU', 'content': '交易无明显波动，但航旅快捷产品结构有变化，变化值为1091.73%，请关注。', 'content_rich': '波动详情：      交易无明显波动，但航旅快捷产品结构有变化，变化值为<text_tag color=carmine>1091.73%</text_tag>，请关注。', 'type': '商户签约名'}, {'name': '张涛', 'title': '商户（收方或付方）产品波动异常', 'customer_name': 'CZ', 'content': '交易无明显波动，但会员产品结构有变化，变化值为1620.69%，请关注。', 'content_rich': '波动详情：      交易无明显波动，但会员产品结构有变化，变化值为<text_tag color=carmine>1620.69%</text_tag>，请关注。', 'type': '商户签约名'}, {'name': '张涛', 'title': '商户（收方或付方）产品波动异常', 'customer_name': 'CZ', 'content': '交易无明显波动，但旗舰店产品结构有变化，变化值为1333.70%，请关注。', 'content_rich': '波动详情：      交易无明显波动，但旗舰店产品结构有变化，变化值为<text_tag color=carmine>1333.70%</text_tag>，请关注。', 'type': '商户签约名'}, {'name': '张涛', 'title': '商户（收方或付方）产品波动异常', 'customer_name': '苏南瑞丽航空有限公司', 'content': '交易无明显波动，但会员产品结构有变化，变化值为227647.68%，请关注。', 'content_rich': '波动详情：      交易无明显波动，但会员产品结构有变化，变化值为<text_tag color=carmine>227647.68%</text_tag>，请关注。', 'type': '商户签约名'}, {'name': '张涛', 'title': '商户（收方或付方）产品波动异常', 'customer_name': 'G5', 'content': '交易无明显波动，但聚合产品结构有变化，变化值为288.51%，请关注。', 'content_rich': '波动详情：      交易无明显波动，但聚合产品结构有变化，变化值为<text_tag color=carmine>288.51%</text_tag>，请关注。', 'type': '商户签约名'}, {'name': '张涛', 'title': '商户（收方或付方）产品波动异常', 'customer_name': 'G5', 'content': '交易无明显波动，但旗舰店产品结构有变化，变化值为4310.09%，请关注。', 'content_rich': '波动详情：      交易无明显波动，但旗舰店产品结构有变化，变化值为<text_tag color=carmine>4310.09%</text_tag>，请关注。', 'type': '商户签约名'}, {'name': '张涛', 'title': '商户（收方或付方）产品波动异常', 'customer_name': 'A6', 'content': '交易无明显波动，但会员产品结构有变化，变化值为54626.43%，请关注。', 'content_rich': '波动详情：      交易无明显波动，但会员产品结构有变化，变化值为<text_tag color=carmine>54626.43%</text_tag>，请关注。', 'type': '商户签约名'}, {'name': '张涛', 'title': '商户（收方或付方）产品波动异常', 'customer_name': 'A6', 'content': '交易无明显波动，但网银产品结构有变化，变化值为53739.18%，请关注。', 'content_rich': '波动详情：      交易无明显波动，但网银产品结构有变化，变化值为<text_tag color=carmine>53739.18%</text_tag>，请关注。', 'type': '商户签约名'}, {'name': '段超', 'title': '商户（收方或付方）产品波动异常', 'customer_name': 'KN', 'content': '交易无明显波动，但会员产品结构有变化，变化值为29913.84%，请关注。', 'content_rich': '波动详情：      交易无明显波动，但会员产品结构有变化，变化值为<text_tag color=carmine>29913.84%</text_tag>，请关注。', 'type': '商户签约名'}, {'name': '段超', 'title': '商户（收方或付方）产品波动异常', 'customer_name': 'KN', 'content': '交易无明显波动，但航旅快捷产品结构有变化，变化值为8559.02%，请关注。', 'content_rich': '波动详情：      交易无明显波动，但航旅快捷产品结构有变化，变化值为<text_tag color=carmine>8559.02%</text_tag>，请关注。', 'type': '商户签约名'}, {'name': '王琦-3', 'title': '商户（收方或付方）产品波动异常', 'customer_name': 'MU-2', 'content': '交易无明显波动，但会员产品结构有变化，变化值为5319.54%，请关注。', 'content_rich': '波动详情：      交易无明显波动，但会员产品结构有变化，变化值为<text_tag color=carmine>5319.54%</text_tag>，请关注。', 'type': '商户签约名'}, {'name': '吴昊', 'title': '商户（收方或付方）产品波动异常', 'customer_name': 'TV', 'content': '交易无明显波动，但会员产品结构有变化，变化值为1713.39%，请关注。', 'content_rich': '波动详情：      交易无明显波动，但会员产品结构有变化，变化值为<text_tag color=carmine>1713.39%</text_tag>，请关注。', 'type': '商户签约名'}, {'name': '吴昊', 'title': '商户（收方或付方）产品波动异常', 'customer_name': 'TV', 'content': '交易无明显波动，但航旅快捷产品结构有变化，变化值为3301.69%，请关注。', 'content_rich': '波动详情：      交易无明显波动，但航旅快捷产品结构有变化，变化值为<text_tag color=carmine>3301.69%</text_tag>，请关注。', 'type': '商户签约名'}, {'name': '吴昊', 'title': '商户（收方或付方）产品波动异常', 'customer_name': '3U', 'content': '交易无明显波动，但网银产品结构有变化，变化值为288.66%，请关注。', 'content_rich': '波动详情：      交易无明显波动，但网银产品结构有变化，变化值为<text_tag color=carmine>288.66%</text_tag>，请关注。', 'type': '商户签约名'}, {'name': '林源涛', 'title': '商户（收方或付方）产品波动异常', 'customer_name': '北京一百伟业信息技术有限公司', 'content': '交易无明显波动，但航旅快捷产品结构有变化，变化值为86.37%，请关注。', 'content_rich': '波动详情：      交易无明显波动，但航旅快捷产品结构有变化，变化值为<text_tag color=orange>86.37%</text_tag>，请关注。', 'type': '付方签约名'}, {'name': '林源涛', 'title': '商户（收方或付方）产品波动异常', 'customer_name': '广州百奕信息科技有限公司', 'content': '交易无明显波动，但航旅快捷产品结构有变化，变化值为391.80%，请关注。', 'content_rich': '波动详情：      交易无明显波动，但航旅快捷产品结构有变化，变化值为<text_tag color=carmine>391.80%</text_tag>，请关注。', 'type': '付方签约名'}, {'name': '段超', 'title': '商户（收方或付方）产品波动异常', 'customer_name': '北京小桔国际旅行社有限公司', 'content': '交易无明显波动，但会员产品结构有变化，变化值为5183.64%，请关注。', 'content_rich': '波动详情：      交易无明显波动，但会员产品结构有变化，变化值为<text_tag color=carmine>5183.64%</text_tag>，请关注。', 'type': '付方签约名'}, {'name': None, 'title': '商户（收方或付方）产品波动异常', 'customer_name': '云南东翔商务有限公司', 'content': '交易无明显波动，但会员产品结构有变化，变化值为462.11%，请关注。', 'content_rich': '波动详情：      交易无明显波动，但会员产品结构有变化，变化值为<text_tag color=carmine>462.11%</text_tag>，请关注。', 'type': '付方签约名'}, {'name': None, 'title': '商户（收方或付方）产品波动异常', 'customer_name': '上海恒顺旅行（集团）有限公司', 'content': '交易无明显波动，但会员产品结构有变化，变化值为3459.09%，请关注。', 'content_rich': '波动详情：      交易无明显波动，但会员产品结构有变化，变化值为<text_tag color=carmine>3459.09%</text_tag>，请关注。', 'type': '付方签约名'}, {'name': None, 'title': '商户（收方或付方）产品波动异常', 'customer_name': '广州百奕信息科技有限公司', 'content': '交易无明显波动，但航旅快捷产品结构有变化，变化值为391.80%，请关注。', 'content_rich': '波动详情：      交易无明显波动，但航旅快捷产品结构有变化，变化值为<text_tag color=carmine>391.80%</text_tag>，请关注。', 'type': '付方签约名'}, {'name': None, 'title': '商户（收方或付方）产品波动异常', 'customer_name': '浙江星翔航空票务有限公司', 'content': '交易无明显波动，但航旅快捷产品结构有变化，变化值为117.33%，请关注。', 'content_rich': '波动详情：      交易无明显波动，但航旅快捷产品结构有变化，变化值为<text_tag color=carmine>117.33%</text_tag>，请关注。', 'type': '付方签约名'}, {'name': None, 'title': '商户（收方或付方）产品波动异常', 'customer_name': '北京小桔国际旅行社有限公司', 'content': '交易无明显波动，但会员产品结构有变化，变化值为5183.64%，请关注。', 'content_rich': '波动详情：      交易无明显波动，但会员产品结构有变化，变化值为<text_tag color=carmine>5183.64%</text_tag>，请关注。', 'type': '付方签约名'}, {'name': None, 'title': '商户（收方或付方）产品波动异常', 'customer_name': '上海凌程航空票务服务有限公司', 'content': '交易无明显波动，但会员产品结构有变化，变化值为3528.28%，请关注。', 'content_rich': '波动详情：      交易无明显波动，但会员产品结构有变化，变化值为<text_tag color=carmine>3528.28%</text_tag>，请关注。', 'type': '付方签约名'}, {'name': None, 'title': '商户（收方或付方）产品波动异常', 'customer_name': '武汉市胜意之旅旅行社有限公司', 'content': '交易无明显波动，但会员产品结构有变化，变化值为384.54%，请关注。', 'content_rich': '波动详情：      交易无明显波动，但会员产品结构有变化，变化值为<text_tag color=carmine>384.54%</text_tag>，请关注。', 'type': '付方签约名'}, {'name': None, 'title': '商户（收方或付方）产品波动异常', 'customer_name': '重庆小鸟集合国际旅行社有限公司', 'content': '交易无明显波动，但会员产品结构有变化，变化值为1498.96%，请关注。', 'content_rich': '波动详情：      交易无明显波动，但会员产品结构有变化，变化值为<text_tag color=carmine>1498.96%</text_tag>，请关注。', 'type': '付方签约名'}, {'name': None, 'title': '商户（收方或付方）产品波动异常', 'customer_name': '北京一百伟业信息技术有限公司', 'content': '交易无明显波动，但航旅快捷产品结构有变化，变化值为86.37%，请关注。', 'content_rich': '波动详情：      交易无明显波动，但航旅快捷产品结构有变化，变化值为<text_tag color=orange>86.37%</text_tag>，请关注。', 'type': '付方签约名'}, {'name': None, 'title': '商户（收方或付方）产品波动异常', 'customer_name': '上海顺行天下票务代理有限公司', 'content': '交易无明显波动，但会员产品结构有变化，变化值为7469.30%，请关注。', 'content_rich': '波动详情：      交易无明显波动，但会员产品结构有变化，变化值为<text_tag color=carmine>7469.30%</text_tag>，请关注。', 'type': '付方签约名'}, {'name': '吴昊', 'title': '商户（收方或付方）产品波动异常', 'customer_name': '云南东翔商务有限公司', 'content': '交易无明显波动，但会员产品结构有变化，变化值为462.11%，请关注。', 'content_rich': '波动详情：      交易无明显波动，但会员产品结构有变化，变化值为<text_tag color=carmine>462.11%</text_tag>，请关注。', 'type': '付方签约名'}, {'name': '吴昊', 'title': '商户（收方或付方）产品波动异常', 'customer_name': '重庆小鸟集合国际旅行社有限公司', 'content': '交易无明显波动，但会员产品结构有变化，变化值为1498.96%，请关注。', 'content_rich': '波动详情：      交易无明显波动，但会员产品结构有变化，变化值为<text_tag color=carmine>1498.96%</text_tag>，请关注。', 'type': '付方签约名'}, {'name': '原泉', 'title': '商户（收方或付方）产品波动异常', 'customer_name': '武汉市胜意之旅旅行社有限公司', 'content': '交易无明显波动，但会员产品结构有变化，变化值为384.54%，请关注。', 'content_rich': '波动详情：      交易无明显波动，但会员产品结构有变化，变化值为<text_tag color=carmine>384.54%</text_tag>，请关注。', 'type': '付方签约名'}, {'name': '李志兰', 'title': '商户（收方或付方）产品波动异常', 'customer_name': '上海恒顺旅行（集团）有限公司', 'content': '交易无明显波动，但会员产品结构有变化，变化值为3459.09%，请关注。', 'content_rich': '波动详情：      交易无明显波动，但会员产品结构有变化，变化值为<text_tag color=carmine>3459.09%</text_tag>，请关注。', 'type': '付方签约名'}, {'name': '李志兰', 'title': '商户（收方或付方）产品波动异常', 'customer_name': '上海顺行天下票务代理有限公司', 'content': '交易无明显波动，但会员产品结构有变化，变化值为7469.30%，请关注。', 'content_rich': '波动详情：      交易无明显波动，但会员产品结构有变化，变化值为<text_tag color=carmine>7469.30%</text_tag>，请关注。', 'type': '付方签约名'}, {'name': '李志兰', 'title': '商户（收方或付方）产品波动异常', 'customer_name': '上海凌程航空票务服务有限公司', 'content': '交易无明显波动，但会员产品结构有变化，变化值为3528.28%，请关注。', 'content_rich': '波动详情：      交易无明显波动，但会员产品结构有变化，变化值为<text_tag color=carmine>3528.28%</text_tag>，请关注。', 'type': '付方签约名'}, {'name': '李志兰', 'title': '商户（收方或付方）产品波动异常', 'customer_name': '浙江星翔航空票务有限公司', 'content': '交易无明显波动，但航旅快捷产品结构有变化，变化值为117.33%，请关注。', 'content_rich': '波动详情：      交易无明显波动，但航旅快捷产品结构有变化，变化值为<text_tag color=carmine>117.33%</text_tag>，请关注。', 'type': '付方签约名'}]
#
#
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
#         # 构建内容字符串
#         content = (
#             f"Name: {item['name']}\n"
#             f"Title: {item['title']}\n"
#             f"Content: {item['content']}\n"
#             f"Customer_name: {item['customer_name']}\n"
#             f"Type: {item['type']}\n"
#
#         )
#
#         # 调用存储消息的函数
#         store_his_message(
#             app_chat_service,
#             sender_open_id=sender_open_id,
#             sales=item['name'],
#             title=item['title'],
#             content=content,
#             merchant_no=item['customer_name'],
#             product=item['type'],
#             display_type="hanglv_card",
#
#         )
#
#
#     # 按名字过滤数据
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
#     # 发送消息
#     for name, reports in name_to_data.items():
#         conv_id_map = hanglv_api_use.get_user_open_id(name = "张华雪")
#         for email, conv_id in conv_id_map.items():
#             content = card_templates.travel_report_content3(
#                 template_variable={
#                     "unlike_callback_event": {
#                         "event_type": "unlike",
#                         "event_source": "",
#                         "event_data": {
#                             "message": "航旅波动检测归因3"
#                         }
#                     },
#                     "travel_report_list": reports,  # 将所有报告传递给模板
#                     "title": reports[0]['title'],  # 使用第一个报告的标题
#                     "name": name
#                 }
#             )
#
#             # 添加调试信息，打印生成的内容
#             print("Sending to:", name, "Conv ID:", conv_id)
#             print("Generated Content:", content)
#
#             resp = lark_message_util.send_card_message(
#                 receive_id=conv_id,  # 使用 conv_id 作为接收者的 ID
#                 content=content
#             )
#             print("发送的卡片信息是：", resp)
#



