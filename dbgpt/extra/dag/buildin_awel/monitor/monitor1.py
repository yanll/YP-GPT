from dbgpt.extra.dag.buildin_awel.monitor import monitor1_data


def monitor1():


    d_1_trx_date = '2024-05-24'
    d_1_d_7_trx_date = '2024-05-24,2024-05-23,2024-05-22,2024-05-21,2024-05-20,2024-05-17,2024-05-17'

    try:
        print('开始获取监控二所需数据')
        d_1_data = monitor1_data.get_data_by_stat_in_monitor1(d_1_trx_date)
        d_1_d_7_data = monitor1_data.get_data_by_stat_in_monitor1(d_1_d_7_trx_date)
    except Exception as e:
        print('监控获取数据异常')
        raise e

    print('监控一开始判断预警')
    alert_list = []

    return alert_list

