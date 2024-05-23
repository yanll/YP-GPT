from dbgpt.extra.dag.buildin_awel.monitor import monitor2_data


def monitor2():

    trx_date = '2024-05-22'
    try:
        print('开始获取监控二所需数据')
        last_week_data = monitor2_data.get_refund_rate_in_monitor2(trx_date)
    except Exception as e:
        print('监控获取数据异常')
        raise e

    alert_list = []
    for item in last_week_data:
        STAT_DISPAYSIGNEDNAME = item['STAT_DISPAYSIGNEDNAME']
        REFUND_RATE = float(item['REFUND_RATE'])
        if REFUND_RATE > 0.3:
            alert_list.append({
                'name': monitor2_data.search_by_stat_dispaysignedname(STAT_DISPAYSIGNEDNAME)[0]['SALES_NAME'],
                'title': '退款笔数波动异常',
                'content': f'商户签约名:{STAT_DISPAYSIGNEDNAME}，昨日退款波动超过30%，退款率{REFUND_RATE:.2f}，请关注'
            })

    return alert_list