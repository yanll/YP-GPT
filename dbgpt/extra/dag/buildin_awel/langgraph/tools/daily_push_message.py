#
# import requests
# import json
# from datetime import datetime, timedelta
#
# from dbgpt.extra.dag.buildin_awel.langgraph.wrappers.daily_push_messages import result_yesterday, \
#     result_day_before_yesterday, profit_yesterday, profit_day_before_yesterday, profit_day7_before_yesterday, \
#     average_day7_before_yesterday
#
#
# def get_previous_dates():
#     today = datetime.now()
#     yesterday = today - timedelta(days=1)
#     day7_before_yesterday = today - timedelta(days=7)
#     day_before_yesterday = today - timedelta(days=2)
#     weekly_before_today = yesterday - timedelta(days=7)
#     return yesterday.strftime('%Y-%m-%d'), day_before_yesterday.strftime('%Y-%m-%d'), day7_before_yesterday.strftime('%Y-%m-%d'),weekly_before_today.strftime('%Y-%m-%d')
#
# def maolicase(trx_date):
#     url = 'https://atmgw.yeepay.com/cem-api/mobile/aggScript/wrap/apis/receive/handleApplicationMarketplace/hv_jf_day_summary_situate_one'
#
#     headers = {
#         'Yuiassotoken': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJsb2dpbl90eXBlIjoiQUNDT1VOVCIsIm1vYmlsZSI6IjE4NzU0MzE2MjQwIiwibWlncmF0ZV91c2VyX2lkIjoiZWM4Z2ExYWYiLCJ4LWlwIjoiMTcyLjI1LjI1LjEwIiwicHJpbmNpcGFsX2lkIjoiMTc3OTUiLCJ0b2tlbiI6ImRmNTQwOGNmLTUxNGEtNDAyNS05NDQ0LTNmMDIxNTg2MjliZiIsImxvZ2luX25hbWUiOiJodWF4dWUuemhhbmciLCJ0d29fZmFjdG9yX3ZhbGlkIjp0cnVlLCJsb2dpbl90aW1lIjoiMjAyNC0wNS0xNiAxMzo1MDo0NiIsInNjb3BlIjoiIiwiY2FsbGJhY2siOiJodHRwczovL25jY2VtcG9ydGFsLnllZXBheS5jb20vIy93b3Jrc3BhY2Uvd29ya3NwYWNlIiwic3NvdGlja2V0IjoiYTNhNzgyYzItYWFjMC00ZGIxLWFjZWItMjdlZWRkYTk3NDI5IiwiZXhwIjoxNzE1OTI1MDQ2LCJpYXQiOjE3MTU4MzY4NDYsImVtYWlsIjoiaHVheHVlLnpoYW5nQHllZXBheS5jb20iLCJ1c2VybmFtZSI6IuW8oOWNjumbqiJ9.0bA1ziDRVPYSSpFhEGhUGGQPFkLYL31RfcB51QkM4GRvenUQdVYfK4XMpV0rvrSixmQ8Xc_j85WN9d3KNVpqiQ',  # 省略你的token
#         'pageType': 'cemPortal',
#         'Content-Type': 'application/json',
#         'Cookie': 'JSESSIONID=9C250741FC6942D63FD3A9210E5F4A31'
#     }
#
#     data = {
#         "parameters": {
#             "TYPE": "航司,渠道,酒旅出行",
#             "SCALE_TYPE": "DAY",
#             "TRX_DATE": trx_date,
#             "STAT_SALES_NAME": "段超"
#         },
#         "strategyKey": "saleOrdinaryApplicationMarketExecutor"
#     }
#
#     response = requests.post(url, headers=headers, data=json.dumps(data))
#
#     return response.json()
#
# def format_profit(profit):
#     formatted_profit = f"{profit / 10000:.2f}"  # 转换为万元并保留两位小数
#     formatted_profit = format(float(formatted_profit), ',')  # 添加千分位
#     return formatted_profit
#
# def shujuqingk():
#     # 获取昨天和前天的日期
#     yesterday, day_before_yesterday, day7_before_yesterday,weekly_before_today = get_previous_dates()
#
#     # 构造时间参数
#     trx_date_yesterday = f"{yesterday},{yesterday}"
#     trx_date_day_before_yesterday = f"{day_before_yesterday},{day_before_yesterday}"
#     trx_date_day7_before_yesterday = f"{day7_before_yesterday},{yesterday}"
#     trx_date_weekly_before_today = f"{weekly_before_today},{yesterday}"
#
#
#
#     result_yesterday = maolicase(trx_date_yesterday)
#     result_day_before_yesterday = maolicase(trx_date_day_before_yesterday)
#     result_day7_before_yesterday = maolicase(trx_date_day7_before_yesterday)
#     result_weekly_before_today = maolicase(trx_date_weekly_before_today)
#     average_day7_before_yesterday = format_profit(result_day7_before_yesterday['data']['TRX_PROFIT'] / 7)
#
#     # 提取毛利数据
#     profit_yesterday = format_profit(result_yesterday['data']['TRX_PROFIT'])
#     profit_day_before_yesterday = format_profit(result_day_before_yesterday['data']['TRX_PROFIT'])
#     profit_day7_before_yesterday = format_profit(result_day7_before_yesterday['data']['TRX_PROFIT'])
#     #profit_weekly_before_today = format_profit(result_weekly_before_today['data']['TRX_PROFIT'])
#
#     #昨天相对于前天的同比变化率
#     profit_yesterday_x = float(result_yesterday['data']['TRX_PROFIT'])
#     profit_day_before_yesterday_x = float(result_day_before_yesterday['data']['TRX_PROFIT'])
#     yesterday_change_rate = ((profit_yesterday_x - profit_day_before_yesterday_x) / profit_day_before_yesterday_x) * 100
#     yesterday_change_rate_formatted = "{:.2f}%".format(yesterday_change_rate)
#     # # 上周同一时间的毛利变化率
#     # profit_yesterday_x = float(result_yesterday['data']['TRX_PROFIT'])
#     # profit_weekly_before_today_x = float(result_weekly_before_today['data']['TRX_PROFIT'])
#     # weekly_change_rate = ((profit_yesterday_x - profit_weekly_before_today_x) / profit_weekly_before_today_x) * 100
#     # weekly_change_rate_formatted = "{:.2f}%".format(weekly_change_rate)
#
#     # 上周同一时间的毛利变化率
#     profit_weekly_before_today_x = float(result_weekly_before_today['data']['TRX_PROFIT'])
#     weekly_change_rate = ((profit_yesterday_x - profit_weekly_before_today_x) / profit_weekly_before_today_x) * 100
#     weekly_change_rate_formatted = "{:.2f}%".format(weekly_change_rate)
#     print("上周结果",weekly_change_rate_formatted)
#
#     # 构造结果字典
#     results = {
#         "昨天的毛利": profit_yesterday,
#         "前天的毛利": profit_day_before_yesterday,
#         "昨天相对于前天的同比变化率": yesterday_change_rate_formatted,
#         "上周同一时间的毛利变化率": weekly_change_rate_formatted,
#         "前7天的毛利总额": profit_day7_before_yesterday,
#         "前7天的平均毛利": average_day7_before_yesterday
#     }
#
#     return results
#
# # 在外部文件中调用示例
# # from your_module import shujuqingk
# # data = shujuqingk()
# # print(data)
