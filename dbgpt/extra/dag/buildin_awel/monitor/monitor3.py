from dbgpt.extra.dag.buildin_awel.monitor import monitor3_data

def find_success_amount_by_customer_and_product(data, customer, product, customer_type) -> float:
    for item in data:
        if item[customer_type] == customer and item['PRODUCT'] == product:
            return float(item['SUCCESS_AMOUNT'])
    return 0

def deal_data(alert_list, d_1_data, d_2_data, customer_type):
    customer_list = set()
    product_list = set()
    d_1_customer_success_amount = {}
    d_2_customer_success_amount = {}
    for item in d_1_data:
        product_list.add(item['PRODUCT'])
        customer_list.add(item[customer_type])
        if item[customer_type] not in d_1_customer_success_amount:
            d_1_customer_success_amount[item[customer_type]] = 0
        if item[customer_type] not in d_2_customer_success_amount:
            d_2_customer_success_amount[item[customer_type]] = 0
        d_1_customer_success_amount[item[customer_type]] += float(item['SUCCESS_AMOUNT'])

    for item in d_2_data:
        product_list.add(item['PRODUCT'])
        customer_list.add(item[customer_type])
        if item[customer_type] not in d_2_customer_success_amount:
            d_2_customer_success_amount[item[customer_type]] = 0
        if item[customer_type] not in d_1_customer_success_amount:
            d_1_customer_success_amount[item[customer_type]] = 0
        d_2_customer_success_amount[item[customer_type]] += float(item['SUCCESS_AMOUNT'])

    for customer in customer_list:
        # 规则中没写除0的情况，此处直接抛弃
        if d_1_customer_success_amount[customer] ==0 or d_2_customer_success_amount[customer] ==0:
            continue
        for product in product_list:
            # 环比差值
            difference1 = find_success_amount_by_customer_and_product(d_1_data, customer, product, customer_type)/d_1_customer_success_amount[customer] - find_success_amount_by_customer_and_product(d_2_data, customer, product, customer_type)/d_2_customer_success_amount[customer]
            # 交易量差值_
            difference2 = find_success_amount_by_customer_and_product(d_1_data, customer, product, customer_type)-find_success_amount_by_customer_and_product(d_2_data, customer, product, customer_type)
            # if abs(difference1) > 0.6 and abs(difference2) >= 100000:
            # 测试使用更低的阈值
            if abs(difference1) > 0.1 and abs(difference2) >= 100000:
                if customer_type=='STAT_DISPAYSIGNEDNAME':
                    sale_name = monitor3_data.search_by_stat_dispaysignedname(customer)[0]['SALES_NAME']
                else:
                    sale_name = monitor3_data.search_by_payer_customer_signedname(customer)[0]['PAYER_SALES_NAME']
                alert_list.append({
                    'name': sale_name,
                    'title': '商户（收方或付方）产品波动异常',
                    'customer_name': customer,
                    'content': f'交易无明显波动，但{product}产品结构有变化，变化值为{difference1*100:.2f}%，请关注。',
                    "type": "商户签约名" if customer_type=="STAT_DISPAYSIGNEDNAME" else "付方签约名"
                })

    return alert_list

def monitor3():

    d_1_trx_date = '2024-05-24'
    d_2_trx_date = '2024-05-23'
    try:
        print('开始获取监控三所需数据')
        d_1_data_by_stat = monitor3_data.get_success_amount_by_stat_in_monitor3(d_1_trx_date)
        d_2_data_by_stat = monitor3_data.get_success_amount_by_stat_in_monitor3(d_2_trx_date)

        d_1_data_by_payer = monitor3_data.get_success_amount_by_payer_in_monitor3(d_1_trx_date)
        d_2_data_by_payer = monitor3_data.get_success_amount_by_payer_in_monitor3(d_2_trx_date)
    except Exception as e:
        print('监控三获取数据异常')
        raise e




    print('监控三开始判断预警')
    alert_list = []
    alert_list = deal_data(alert_list, d_1_data_by_stat, d_2_data_by_stat, 'STAT_DISPAYSIGNEDNAME')
    alert_list = deal_data(alert_list, d_1_data_by_payer, d_2_data_by_payer, 'PAYER_CUSTOMER_SIGNEDNAME')

    return alert_list
