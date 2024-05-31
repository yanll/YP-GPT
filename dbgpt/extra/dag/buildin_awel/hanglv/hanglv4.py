import uuid
import logging
from dbgpt.extra.dag.buildin_awel.app.service import AppChatService
from dbgpt.extra.dag.buildin_awel.hanglv import hanglv_api_use
from dbgpt.extra.dag.buildin_awel.lark import card_templates
from dbgpt.extra.dag.buildin_awel.monitor import monitor4
from dbgpt.util.lark import lark_message_util


def store_his_message(app_chat_service, sender_open_id, sales, title, content, product, scene, merchant_no, chanel, display_type):
    rec = {
        "id": str(uuid.uuid1()),
        "agent_name": "SalesAssistant",
        "node_name": "final",
        "conv_uid": sender_open_id,
        "message_type": "view",
        "content": content,
        "message_detail": "",
        "display_type": display_type,
        "biz_date": "12",
        "sales": sales,
        "title": title,
        "scene": scene,
        "chanel": chanel,
        "product": product,
        "merchant_no": merchant_no,
        "reason": "",
        "type": "12",
        "created_time": "",
        "modified_time": "",
    }
    print("rec的值是：", rec)
    try:
        app_chat_service.add_app_hanglv_msg(rec)
    except Exception as e:
        logging.error(f"Error storing message: {e}")

def monitor_four():
    # first = monitor4.Monitor4()
    # hv_data = first.run()
    # print("数值的返回结果", hv_data)
    # data = hv_data
    data = [
        {'name': '段超', 'title': '深航/国航充值业务', 'content': '付方名称:北京嘉信浩远信息技术有限公司，航司:CA——商编:10034228238+场景字段:渠道，近7天充值金额，环比上周下降88.78%，低于大盘82.85%', 'payer_customer_signedname': '北京嘉信浩远信息技术有限公司', 'stat_dispaysignedname': 'CA', 'customer_no': '10034228238', 'payer_business_scene': '渠道', 'sub_content_rich': '波动详情：  近7天充值金额，环比上周下降<text_tag color=red>88.78%</text_tag>，低于大盘<text_tag color=red>82.85%</text_tag>'},
        {'name': '张涛', 'title': '深航/国航充值业务', 'content': '付方名称:新乡市中源航空旅行社有限公司，航司:ZH——商编:10012407595+场景字段:渠道，近7天充值金额，环比上周上升94.90%，高于大盘90.64%', 'payer_customer_signedname': '新乡市中源航空旅行社有限公司', 'stat_dispaysignedname': 'ZH', 'customer_no': '10012407595', 'payer_business_scene': '渠道', 'sub_content_rich': '波动详情：  近7天充值金额，环比上周上升<text_tag color=green>94.90%</text_tag>，高于大盘<text_tag color=green>90.64%</text_tag>'}
    ]

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
            f"Payer Customer Signed Name: {item['payer_customer_signedname']}\n"
            f"Stat Display Signed Name: {item['stat_dispaysignedname']}\n"
            f"Customer No: {item['customer_no']}\n"
            f"Payer Business Scene: {item['payer_business_scene']}\n"
            f"Sub Content Rich: {item['sub_content_rich']}\n"
        )

        # 调用存储消息的函数
        store_his_message(
            app_chat_service,
            sender_open_id=sender_open_id,
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

