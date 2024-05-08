import json
from dbgpt.util.lark import larkutil
from dbgpt.extra.dag.buildin_awel.langgraph.wrappers.crem_30DaysTrxTre_card import \
    get_crem_30DaysTrxTre_card  # 确保此模块路径正确
import logging


def user_crem_30DaysTrxTre_card(open_id, customer_id, customerName,conv_id):  # 添加 conv_id 参数

    try:
        if customer_id == "":
            # 商编ID为空，返回错误消息
            return {"success": False, "response_message": "商编ID不能为空"}

        # 调用外部函数获取商户信息分析结果
        else:
            # customer_id = "KA2022-A09150004"
            customer_analysis = get_crem_30DaysTrxTre_card(open_id, customer_id,customerName)

            print("完整返回结果", customer_analysis)
            # 分解返回结果
            customer_analysis, formatted_data, formatted_data_jiaoyijine, var, var2 = customer_analysis
            acc = json.dumps(var)

            # 检查并打印每个变量以确认内容
            print("Customer Analysis:", customer_analysis)
            print("Formatted Data:", formatted_data)
            print("Formatted Data Jiaoyijine:", formatted_data_jiaoyijine)
            print("Var for chart 1:", var)
            print("Var for chart 2:", var2)
            print("绘图数据", acc)

        # 输出商户信息分析结果
        print("30天毛利与交易金额:", customer_analysis)

        # 发送信息卡片给用户
        larkutil.send_message(
            receive_id=conv_id,
            content=var,
            receive_id_type="open_id",
            msg_type="interactive"
        )
        larkutil.send_message(
            receive_id=conv_id,
            content=var2,
            receive_id_type="open_id",
            msg_type="interactive"
        )

        return {}

    except Exception as e:
        # 记录异常日志并返回错误信息
        logging.error("商户查询工具运行异常：", e)
        return str(e)
