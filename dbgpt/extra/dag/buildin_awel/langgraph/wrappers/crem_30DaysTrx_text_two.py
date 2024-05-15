import logging
from dbgpt.util.lark import lark_message_util
from dbgpt.extra.dag.buildin_awel.lark import card_templates

from dbgpt.extra.dag.buildin_awel.langgraph.wrappers.crem_30DaysTrx_text import get_crem_30DaysTrx_text


def format_num(num):
    if num < 10000:
        return '{:.2f}'.format(num)
    elif num < 100000000:
        return '{:.2f}万'.format(num / 10000)
    else:
        return '{:.2f}亿'.format(num / 100000000)
def format_percent(num):
    return '{:.2%}'.format(num)
def get_crem_30DaysTrx_text_card(open_id=None, customer_id=None, conv_id=None, customer_name=None, ):
    try:
        if customer_id == "" and conv_id == "":
            return {"success": "false", "response_message": "the description of customer_id"}
        data = get_crem_30DaysTrx_text(open_id, customer_id)
        resp_data = [data]
        query_str = (customer_name + "" + "("+customer_id+")").strip()
        print("近30天业务查询结果：", resp_data)
        list = []
        if resp_data and len(resp_data) == 0:
            return {"success": "true", "data": []}
        for m in resp_data:
            jin30tianmaoli = m.get("近30天毛利", "")
            jin30tianmaolipaiming = m.get("近30天毛利排名", "")
            jin30tianjiaoyijine = m.get("近30天交易金额", "")
            jin30tianzhifuchenggonglv = m.get("近30天支付成功率", "")
            list.append({
                "jin30tianmaoli": format_num(float(jin30tianmaoli)) if jin30tianmaoli else "",
                "jin30tianmaolipaiming": jin30tianmaolipaiming,
                "jin30tianjiaoyijine": format_num(float(jin30tianjiaoyijine)) if jin30tianjiaoyijine else "",
                "jin30tianzhifuchenggonglv": format_percent(float(jin30tianzhifuchenggonglv)) if jin30tianzhifuchenggonglv else "",
            })


        da= {
             "list": list,
             "query_str": query_str
        }
        # 发送信息卡片给用户
        lark_message_util.send_card_message(
            receive_id=conv_id,
            content=card_templates.crem_30DaysTrx_text_content(
                template_variable={
                    "unlike_callback_event": {
                        "event_type": "unlike",
                        "event_source": "crem_30DaysTrx_text_list",
                        "event_data": {
                            "message": "近30天业务表现列表"
                        }
                    },
                    "crem_30DaysTrx_text_list": da["list"],
                    "query_str": query_str
                }
            )
        )
        # return {
        #     "success": "true",
        #     "error_message": "",
        #     "action": {
        #         "action_name": "send_lark_form_card",
        #         "card_name": "crem_30DaysTrx_text_list"
        #     },
        #     "data": {
        #             "list": list,
        #             "query_str": query_str
        #         }
        # }
    except Exception as e:
        logging.error("近30天业务表现工具运行异常：", e)
        return repr(e)

# # 调用示例
# customer_id = "KA2021-A11221974"  # 这里替换为你要查询的客户商编ID
# result = get_crem_30DaysTrx_text("", customer_id)
# print(result)