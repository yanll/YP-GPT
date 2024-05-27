from dbgpt.extra.dag.buildin_awel.monitor import monitor1_data


def find_avg_success_amount(data, customer, num):
    success_amount = 0
    for item in data:
        if item["STAT_DISPAYSIGNEDNAME"] == customer:
            success_amount += float(item['SUCCESS_AMOUNT'])

    return success_amount/num


def monitor1():


    d_1_trx_date = '2024-05-24'
    d_1_d_7_trx_date = '2024-05-24,2024-05-23,2024-05-22,2024-05-21,2024-05-20,2024-05-17,2024-05-17'
    d_1_d_15_trx_date = '2024-05-24,2024-05-23,2024-05-22,2024-05-21,2024-05-20,2024-05-17,2024-05-17,2024-05-16,2024-05-15,2024-05-14,2024-05-13,2024-05-10,2024-05-09,2024-05-08,2024-05-07,'

    try:
        print('开始获取监控二所需数据')
        d_1_data = monitor1_data.get_data_by_stat_in_monitor1(d_1_trx_date)
        d_1_d_7_data = monitor1_data.get_data_by_stat_in_monitor1(d_1_d_7_trx_date)
        d_1_d_15_data = monitor1_data.get_data_by_stat_in_monitor1(d_1_d_7_trx_date)
    except Exception as e:
        print('监控获取数据异常')
        raise e

    customer_list = set()
    for item in d_1_d_15_data:
        customer_list.add(item['STAT_DISPAYSIGNEDNAME'])

    for customer in customer_list:
        d_1_avg_success_amount = find_avg_success_amount(d_1_data, customer, 1)
        d_1_d_7_avg_success_amount = find_avg_success_amount(d_1_d_7_data, customer, 7)
        d_1_d_15_avg_success_amount = find_avg_success_amount(d_1_d_15_data, customer, 15)

    print('监控一开始判断预警')
    alert_list = []

    return alert_list

