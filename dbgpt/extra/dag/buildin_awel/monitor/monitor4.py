from dbgpt.extra.dag.buildin_awel.monitor import monitor4_data


def deal_customer(alert_list, CUSTOMER, sale_name, customer_no, stat_dispaysignedname):
    for PAYER_CUSTOMER_SIGNEDNAME in CUSTOMER['PAYER_CUSTOMER_SIGNEDNAME_list']:
        if PAYER_CUSTOMER_SIGNEDNAME not in CUSTOMER['PAYER_CUSTOMER_SIGNEDNAME_to_SUCCESS_AMOUNT_this_week']:
            CUSTOMER['PAYER_CUSTOMER_SIGNEDNAME_to_SUCCESS_AMOUNT_this_week'][PAYER_CUSTOMER_SIGNEDNAME] = 0
        if PAYER_CUSTOMER_SIGNEDNAME not in CUSTOMER['PAYER_CUSTOMER_SIGNEDNAME_to_SUCCESS_AMOUNT_last_week']:
            CUSTOMER['PAYER_CUSTOMER_SIGNEDNAME_to_SUCCESS_AMOUNT_last_week'][PAYER_CUSTOMER_SIGNEDNAME] = 0
        # 警告判断

    # 遍历CUSTOMER
    for PAYER_CUSTOMER_SIGNEDNAME in CUSTOMER['PAYER_CUSTOMER_SIGNEDNAME_list']:
        PAYER_CUSTOMER_SIGNEDNAME_to_SUCCESS_AMOUNT_this_week = \
        CUSTOMER['PAYER_CUSTOMER_SIGNEDNAME_to_SUCCESS_AMOUNT_this_week'][PAYER_CUSTOMER_SIGNEDNAME]
        PAYER_CUSTOMER_SIGNEDNAME_to_SUCCESS_AMOUNT_last_week = \
        CUSTOMER['PAYER_CUSTOMER_SIGNEDNAME_to_SUCCESS_AMOUNT_last_week'][PAYER_CUSTOMER_SIGNEDNAME]
        content = None

        if PAYER_CUSTOMER_SIGNEDNAME_to_SUCCESS_AMOUNT_last_week == 0:
            if PAYER_CUSTOMER_SIGNEDNAME_to_SUCCESS_AMOUNT_this_week >= 50 * (10 ** 4):
                content = f'付方名称:{PAYER_CUSTOMER_SIGNEDNAME}，航司:{stat_dispaysignedname}——商编:{customer_no}+场景字段，近7天充值金额为{PAYER_CUSTOMER_SIGNEDNAME_to_SUCCESS_AMOUNT_this_week}，近7天充值金额为{PAYER_CUSTOMER_SIGNEDNAME_to_SUCCESS_AMOUNT_last_week}'
        else:
            fluctuation = (PAYER_CUSTOMER_SIGNEDNAME_to_SUCCESS_AMOUNT_this_week /
                           PAYER_CUSTOMER_SIGNEDNAME_to_SUCCESS_AMOUNT_last_week) - (
                                      CUSTOMER['SUCCESS_AMOUNT_this_week'] / CUSTOMER['SUCCESS_AMOUNT_last_week'])

            if PAYER_CUSTOMER_SIGNEDNAME_to_SUCCESS_AMOUNT_this_week >= 1500 * (10 ** 4):
                if fluctuation <= -0.15:
                    content = f'付方名称:{PAYER_CUSTOMER_SIGNEDNAME}，航司:{stat_dispaysignedname}——商编:{customer_no}+场景字段，近7天充值金额，环比上周下降{fluctuation * 100:.2f}%，高于/低于大盘**'
                if fluctuation >= 0.20:
                    content = f'付方名称:{PAYER_CUSTOMER_SIGNEDNAME}，航司:{stat_dispaysignedname}——商编:{customer_no}+场景字段，近7天充值金额，环比上周上升{fluctuation * 100:.2f}%，高于/低于大盘**'
            elif PAYER_CUSTOMER_SIGNEDNAME_to_SUCCESS_AMOUNT_this_week < 1500 * (
                    10 ** 4) and PAYER_CUSTOMER_SIGNEDNAME_to_SUCCESS_AMOUNT_this_week >= 100 * (10 ** 4):
                if fluctuation <= -0.50:
                    content = f'付方名称:{PAYER_CUSTOMER_SIGNEDNAME}，航司:{stat_dispaysignedname}——商编:{customer_no}+场景字段，近7天充值金额，环比上周下降{fluctuation * 100:.2f}%，高于/低于大盘**'
                if fluctuation >= 0.50:
                    content = f'付方名称:{PAYER_CUSTOMER_SIGNEDNAME}，航司:{stat_dispaysignedname}——商编:{customer_no}+场景字段，近7天充值金额，环比上周上升{fluctuation * 100:.2f}%，高于/低于大盘**'
            elif PAYER_CUSTOMER_SIGNEDNAME_to_SUCCESS_AMOUNT_this_week < 100 * (
                    10 ** 4) and PAYER_CUSTOMER_SIGNEDNAME_to_SUCCESS_AMOUNT_this_week >= 50 * (10 ** 4):
                if fluctuation <= -0.80:
                    content = f'付方名称:{PAYER_CUSTOMER_SIGNEDNAME}，航司:{stat_dispaysignedname}——商编:{customer_no}+场景字段，近7天充值金额，环比上周下降{fluctuation * 100:.2f}%，高于/低于大盘**'
                if fluctuation >= 0.80:
                    content = f'付方名称:{PAYER_CUSTOMER_SIGNEDNAME}，航司:{stat_dispaysignedname}——商编:{customer_no}+场景字段，近7天充值金额，环比上周上升{fluctuation * 100:.2f}%，高于/低于大盘**'

        if content is not None:
            alert_list.append({'name': sale_name, 'title': '深航/国航充值业务',
                               'content': content})

    return alert_list

def monitor4():
    try:
        print('开始获取监控四所需数据')
        this_week_data = monitor4_data.get_this_week_data_in_monitor4()
        last_week_data = monitor4_data.get_last_week_data_in_monitor4()
        sale_name1 = monitor4_data.search_by_customer_no('10012407595')[0]['SALES_NAME']
        sale_name2 = monitor4_data.search_by_customer_no('10034228238')[0]['SALES_NAME']
    except Exception as e:
        print('监控四获取数据异常')
        raise e

    # 收方商编=10012407595为CUSTOMER1
    customer_no1 = '10012407595'
    stat_dispaysignedname1 = 'ZH'
    CUSTOMER1 = {}
    CUSTOMER1['PAYER_CUSTOMER_SIGNEDNAME_list'] = set()
    CUSTOMER1['SUCCESS_AMOUNT_this_week'] = 0
    CUSTOMER1['SUCCESS_AMOUNT_last_week'] = 0
    CUSTOMER1['PAYER_CUSTOMER_SIGNEDNAME_to_SUCCESS_AMOUNT_this_week'] = {}
    CUSTOMER1['PAYER_CUSTOMER_SIGNEDNAME_to_SUCCESS_AMOUNT_last_week'] = {}
    # 收方商编=10034228238为CUSTOMER2
    customer_no2 = '10034228238'
    stat_dispaysignedname2 = 'CA'
    CUSTOMER2 = {}
    CUSTOMER2['PAYER_CUSTOMER_SIGNEDNAME_list'] = set()
    CUSTOMER2['SUCCESS_AMOUNT_this_week'] = 0
    CUSTOMER2['SUCCESS_AMOUNT_last_week'] = 0
    CUSTOMER2['PAYER_CUSTOMER_SIGNEDNAME_to_SUCCESS_AMOUNT_this_week'] = {}
    CUSTOMER2['PAYER_CUSTOMER_SIGNEDNAME_to_SUCCESS_AMOUNT_last_week'] = {}


    # 整理数据
    for item in this_week_data:
        if item['CUSTOMER_NO'] == '10012407595':
            CUSTOMER1['PAYER_CUSTOMER_SIGNEDNAME_list'].add(item['PAYER_CUSTOMER_SIGNEDNAME'])
            CUSTOMER1['SUCCESS_AMOUNT_this_week'] += float(item['SUCCESS_AMOUNT'])
            CUSTOMER1['PAYER_CUSTOMER_SIGNEDNAME_to_SUCCESS_AMOUNT_this_week'][
                item['PAYER_CUSTOMER_SIGNEDNAME']] = float(item['SUCCESS_AMOUNT'])
        elif item['CUSTOMER_NO'] == '10034228238':
            CUSTOMER2['PAYER_CUSTOMER_SIGNEDNAME_list'].add(item['PAYER_CUSTOMER_SIGNEDNAME'])
            CUSTOMER2['SUCCESS_AMOUNT_this_week'] += float(item['SUCCESS_AMOUNT'])
            CUSTOMER2['PAYER_CUSTOMER_SIGNEDNAME_to_SUCCESS_AMOUNT_this_week'][
                item['PAYER_CUSTOMER_SIGNEDNAME']] = float(item['SUCCESS_AMOUNT'])

    for item in last_week_data:
        if item['CUSTOMER_NO'] == '10012407595':
            CUSTOMER1['PAYER_CUSTOMER_SIGNEDNAME_list'].add(item['PAYER_CUSTOMER_SIGNEDNAME'])
            CUSTOMER1['SUCCESS_AMOUNT_last_week'] += float(item['SUCCESS_AMOUNT'])
            CUSTOMER1['PAYER_CUSTOMER_SIGNEDNAME_to_SUCCESS_AMOUNT_last_week'][
                item['PAYER_CUSTOMER_SIGNEDNAME']] = float(item['SUCCESS_AMOUNT'])
        elif item['CUSTOMER_NO'] == '10034228238':
            CUSTOMER2['PAYER_CUSTOMER_SIGNEDNAME_list'].add(item['PAYER_CUSTOMER_SIGNEDNAME'])
            CUSTOMER2['SUCCESS_AMOUNT_last_week'] += float(item['SUCCESS_AMOUNT'])
            CUSTOMER2['PAYER_CUSTOMER_SIGNEDNAME_to_SUCCESS_AMOUNT_last_week'][
                item['PAYER_CUSTOMER_SIGNEDNAME']] = float(item['SUCCESS_AMOUNT'])

    print('监控四开始判断预警')
    alert_list = []
    alert_list = deal_customer(alert_list, CUSTOMER1, sale_name1, customer_no1, stat_dispaysignedname1)
    alert_list = deal_customer(alert_list, CUSTOMER2, sale_name2, customer_no2, stat_dispaysignedname2)

    return alert_list
