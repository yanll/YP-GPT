
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

def monitor_two():
    hv_data = monitor.main2()
    print("数值的返回结果", hv_data)
    data = hv_data

    # 名字与 conv_id 的对应关系
    name_to_conv_id = {
        '王琦-3': 'ou_9d42bb88ec8940baf3ad183755131881',
        '林源涛': 'ou_9d42bb88ec8940baf3ad183755131881'
    }
    #'wei.huang-1@yeepay.com': 'ou_7acf1ad58a4faa8c60c75d195a9ac220'

    # 按名字过滤数据
    name_to_data = {}
    for report in data:
        name = report['name']
        if name not in name_to_data:
            name_to_data[name] = []
        # 在这里为每个报告添加 num 字段
        report_with_num = report.copy()  # 创建报告的副本，以防止修改原始数据
        report_with_num['num'] = len(name_to_data[name]) + 1  # 添加 num 字段，从 1 开始
        name_to_data[name].append(report_with_num)

    # 发送消息
    for name, reports in name_to_data.items():
        conv_id = name_to_conv_id.get(name)

        if conv_id:
            content = card_templates.travel_report_content2(
                template_variable={
                    "unlike_callback_event": {
                        "event_type": "unlike",
                        "event_source": "",
                        "event_data": {
                            "message": "航旅波动检测归因"
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
# monitor_two()


#
# from typing import List, Dict
# import logging
# from dbgpt.extra.dag.buildin_awel.langgraph.tools.daily_push_message_tool import Dailypushmessagetool
# from dbgpt.core.awel import DAG, HttpTrigger, MapOperator
# from dbgpt.extra.dag.buildin_awel.lark import card_templates
# from dbgpt.storage.metadata import BaseModel
# from dbgpt.util.lark import lark_message_util  # 导入发送卡片的工具类
# from dbgpt.extra.dag.buildin_awel.monitor import monitor
#
# # 名字与 conv_id 的对应关系
# name_to_conv_id = {
#     '王琦-3': 'ou_9d42bb88ec8940baf3ad183755131881',
#     '林源涛': 'ou_9d42bb88ec8940baf3ad183755131881'
# }
#
# class MonitorRequest(BaseModel):
#     pass  # 根据需要定义请求体的数据结构
#
# class RequestHandleOperator(MapOperator[MonitorRequest, List[Dict]]):
#     async def map(self, input_value: MonitorRequest) -> List[Dict]:
#         results = []
#         try:
#             hv_data = monitor.main2()
#             print("数值的返回结果", hv_data)
#             data = hv_data
#
#             # 按名字过滤数据
#             name_to_data = {}
#             for report in data:
#                 name = report['name']
#                 if name not in name_to_data:
#                     name_to_data[name] = []
#                 # 在这里为每个报告添加 num 字段
#                 report_with_num = report.copy()  # 创建报告的副本，以防止修改原始数据
#                 report_with_num['num'] = len(name_to_data[name]) + 1  # 添加 num 字段，从 1 开始
#                 name_to_data[name].append(report_with_num)
#
#             # 发送消息
#             for name, reports in name_to_data.items():
#                 conv_id = name_to_conv_id.get(name)
#                 if conv_id:
#                     content = card_templates.travel_report_content2(
#                         template_variable={
#                             "unlike_callback_event": {
#                                 "event_type": "unlike",
#                                 "event_source": "",
#                                 "event_data": {
#                                     "message": "航旅波动检测归因"
#                                 }
#                             },
#                             "travel_report_list": reports,  # 将所有报告传递给模板
#                             "title": reports[0]['title'],  # 使用第一个报告的标题
#                             "name": name
#                         }
#                     )
#
#                     # 添加调试信息，打印生成的内容
#                     print("Sending to:", name, "Conv ID:", conv_id)
#                     print("Generated Content:", content)
#
#                     resp = lark_message_util.send_card_message(
#                         receive_id=conv_id,  # 使用 conv_id 作为接收者的 ID
#                         content=content
#                     )
#                     print("发送的卡片信息是：", resp)
#                     lark_message_id = resp.get("message_id", "")
#                     print("lark_message_id是：", lark_message_id)
#
#                     results.append({"name": name, "conv_id": conv_id, "lark_message_id": lark_message_id})
#
#         except Exception as e:
#             logging.error(f"Error occurred: {e}")
#             results.append({"error": str(e)})
#
#         return results
#
# with DAG("dbgpt_awel_lark_daily_push_event2") as dag:
#     trigger = HttpTrigger(
#         endpoint="/lark_daily_push_event2",
#         methods="POST",
#         request_body=Dict
#     )
#     map_node = RequestHandleOperator()
#     trigger >> map_node
#
#
# import requests
#
# # 请求的数据，根据你的接口需要进行相应的设置
# data = {
#     }
#
# # 发送 POST 请求
# response = requests.post("http://127.0.0.1:5670/api/v1/awel/trigger/lark_daily_push_event2", json=data)
#
# # 输出响应结果
# print(response.status_code)
# print(response.json())