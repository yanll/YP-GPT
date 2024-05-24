from dbgpt.extra.dag.buildin_awel.langgraph.wrappers.lark_event_handler_wrapper import LarkEventHandlerWrapper
from dbgpt.extra.dag.buildin_awel.lark import card_templates
from dbgpt.extra.dag.buildin_awel.monitor import monitor
from dbgpt.util.lark import lark_message_util
import requests

# data = [
#     {'name': '张涛', 'title': '深航/国航充值业务', 'content': '付方名称:广州市宇翔航空服务有限公司，航司:ZH——商编:10012407595+场景字段，近7天充值金额，环比上周上升267.31%，高于/低于大盘**'},
#     {'name': '张涛', 'title': '深航/国航充值业务', 'content': '付方名称:深圳市广通联旅行社有限公司，航司:ZH——商编:10012407595+场景字段，近7天充值金额，环比上周上升176.17%，高于/低于大盘**'},
#     {'name': '张涛', 'title': '深航/国航充值业务', 'content': '付方名称:北京保盛易行航空服务有限公司，航司:ZH——商编:10012407595+场景字段，近7天充值金额，环比上周上升50.97%，高于/低于大盘**'}
# ]

# hv_data = monitor.main()
# print("数值的返回结果",hv_data)
# resp_data = []
#
# data = hv_data

# data = [
#     {'name': '张三', 'title': '深航/国航充值业务', 'content': '付方名称:广州市宇翔航空服务有限公司，航司:ZH——商编:10012407595+场景字段，近7天充值金额，环比上周上升267.31%，高于/低于大盘**'},
#     {'name': '李四', 'title': '深航/国航充值业务', 'content': '付方名称:深圳市广通联旅行社有限公司，航司:ZH——商编:10012407595+场景字段，近7天充值金额，环比上周上升176.17%，高于/低于大盘**'},
# ]
#
# conv_ids = [
#
#     "ou_9d42bb88ec8940baf3ad183755131881",
#     "ou_a22698cffd738d7851ef30f5dad1a06c"
#
# ]
# conv_id = "ou_9d42bb88ec8940baf3ad183755131881"
#
# lark_message_util.send_card_message(
#     receive_id=conv_id,  # 使用 conv_id 作为接收者的 ID
#     content= card_templates.travel_report_content(
#         template_variable={
#             "unlike_callback_event": {
#                 "event_type": "unlike",
#                 "event_source": "",
#                 "event_data": {
#                     "message": "航旅波动检测归因"
#                 }
#             },
#             "travel_report_list": data,
#         }
#     )
#   )
# data = [{'name': '张涛', 'title': '深航/国航充值业务',
#              'content': '付方名称:广州市宇翔航空服务有限公司，'
#                         '航司:ZH——商编:10012407595+场景字段，'
#                         '近7天充值金额，环比上周上升171.11%，'
#                         '高于/低于大盘**'},
#             {'name': '张涛', 'title': '深航/国航充值业务',
#              'content': '付方名称:深圳市广通联旅行社有限公司，'
#                         '航司:ZH——商编:10012407595+场景字段，'
#                         '近7天充值金额，环比上周上升98.03%，高于/低于大盘**'},
#             {'name': '张涛', 'title': '深航/国航充值业务',
#              'content': '付方名称:苏州市华谊商务有限公司，'
#                         '航司:ZH——商编:10012407595+场景字段，'
#                         '近7天充值金额，环比上周上升677.29%，高于/低于大盘**'},
#             {'name': '张涛', 'title': '深航/国航充值业务',
#              'content': '付方名称:北京保盛易行航空服务有限公司，'
#                         '航司:ZH——商编:10012407595+场景字段，'
#                         '近7天充值金额，环比上周上升88.06%，高于/低于大盘**'},
#             {'name': '张涛', 'title': '深航/国航充值业务',
#              'content': '付方名称:北京东方祥云咨询有限公司，'
#                         '航司:ZH——商编:10012407595+场景字段，'
#                         '近7天充值金额，环比上周上升91.15%，高于/低于大盘**'},
#             {'name': '张涛', 'title': '深航/国航充值业务',
#              'content': '付方名称:重庆云上航空票务股份有限公司，'
#                         '航司:ZH——商编:10012407595+场景字段，'
#                         '近7天充值金额，环比上周上升103.50%，高于/低于大盘**'},
#             {'name': '段超', 'title': '深航/国航充值业务',
#              'content': '付方名称:四川云游九州航空票务服务有限公司，'
#                         '航司:ZH——商编:10034228238+场景字段，'
#                         '近7天充值金额，环比上周上升58.61%，高于/低于大盘**'},
#             {'name': '段超', 'title': '深航/国航充值业务',
#              'content': '付方名称:杭州泛美航空国际旅行社有限公司，'
#                         '航司:ZH——商编:10034228238+场景字段，'
#                         '近7天充值金额，环比上周上升45.72%，高于/低于大盘**'},
#             {'name': '段超', 'title': '深航/国航充值业务',
#              'content': '付方名称:四川铁航航空运输有限公司，'
#                         '航司:ZH——商编:10034228238+场景字段，近7天充值金额，'
#                         '环比上周下降-44.90%，高于/低于大盘**'},
#             {'name': '段超', 'title': '深航/国航充值业务',
#              'content': '付方名称:上海广发航空票务服务有限公司，'
#                         '航司:ZH——商编:10034228238+场景字段，'
#                         '近7天充值金额，环比上周上升47.54%，高于/低于大盘**'}]


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
    # hv_data = monitor.main2()
    # print("数值的返回结果", hv_data)
    # data = hv_data
    #原始数据
    data = [{'name': '王琦-3',
             'title': '退款笔数波动异常',
             'type': '商户签约名',
             'customer_name': '东方航空电子商务有限公司',
             'content': '昨日退款波动超过30%，退款率49.01%，请关注'},
            {'name': '王琦-3',
             'title': '退款笔数波动异常',
             'type': '付方签约名',
             'customer_name': '璟逸鑫（上海）航空服务有限公司',
             'content': '昨日退款波动超过30%，退款率50.00%，请关注'},
            {'name': '王琦-3',
             'title': '退款笔数波动异常',
             'type': '付方签约名',
             'customer_name': '安徽众飞文化旅游发展有限公司',
             'content': '昨日退款波动超过30%，退款率133.33%，请关注'},
            {'name': '林源涛',
             'title': '退款笔数波动异常',
             'type': '付方签约名',
             'customer_name': '巴彦淖尔市小往大来信息科技有限公司',
             'content': '昨日退款波动超过30%，退款率31.62%，请关注'},
            {'name': '林源涛',
             'title': '退款笔数波动异常',
             'type': '付方签约名',
             'customer_name': '北京保盛易行航空服务有限公司',
             'content': '昨日退款波动超过30%，退款率46.79%，请关注'}, ]





    # 名字与 conv_id 的对应关系
    name_to_conv_id = {
        '王琦-3': 'ou_9d42bb88ec8940baf3ad183755131881',
        '林源涛': 'ou_9d42bb88ec8940baf3ad183755131881'
    }

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

            lark_message_id = resp.get("message_id", "")
            print("lark_message_id是：", lark_message_id)




# 调用函数
monitor_two()



