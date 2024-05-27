from dbgpt.extra.dag.buildin_awel.monitor import monitor2_data


def monitor2():

    trx_date = '2024-05-24'
    try:
        print('开始获取监控二所需数据')
        last_day_data_by_stat_dispaysignedname = monitor2_data.get_refund_rate_in_monitor2(trx_date)
        last_day_data_by_payer_customer_signedname = monitor2_data.get_refund_rate_by_payer_in_monitor2(trx_date)
    except Exception as e:
        print('监控获取数据异常')
        raise e

    print('监控二开始判断预警')
    alert_list = []
    for item in last_day_data_by_stat_dispaysignedname:
        STAT_DISPAYSIGNEDNAME = item['STAT_DISPAYSIGNEDNAME']
        REFUND_RATE = float(item['REFUND_RATE'])
        if REFUND_RATE > 0.3:
            alert_list.append({
                'name': monitor2_data.search_by_stat_dispaysignedname(STAT_DISPAYSIGNEDNAME)[0]['SALES_NAME'],
                'title': '退款笔数波动异常',
                'type': '商户签约名',
                'customer_name' : STAT_DISPAYSIGNEDNAME,
                'content': f'昨日退款波动超过30%，退款率{REFUND_RATE*100:.2f}%，请关注'


            })

    for item in last_day_data_by_payer_customer_signedname:
        PAYER_CUSTOMER_SIGNEDNAME = item['PAYER_CUSTOMER_SIGNEDNAME']
        REFUND_RATE = float(item['REFUND_RATE'])
        if PAYER_CUSTOMER_SIGNEDNAME!=0 and REFUND_RATE > 0.3:
            alert_list.append({
                'name': monitor2_data.search_by_payer_customer_signedname(PAYER_CUSTOMER_SIGNEDNAME)[0]['PAYER_SALES_NAME'],
                'title': '退款笔数波动异常',
                'type': '付方签约名',
                'customer_name': PAYER_CUSTOMER_SIGNEDNAME,
                'content': f'昨日退款波动超过30%，退款率{REFUND_RATE*100:.2f}%，请关注'
            })

    return alert_list

# a = monitor2()
# print(a)