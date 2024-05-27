from dbgpt.extra.dag.buildin_awel.monitor import monitor4_data


def find_by_payer_and_stat_dispaysignedname(one_week_data, customer_no, payer_customer_signedname):
    data = {}
    for item in one_week_data:
        if item['CUSTOMER_NO'] == customer_no and item['PAYER_CUSTOMER_SIGNEDNAME'] == payer_customer_signedname:
            data[item['PAYER_BUSINESS_SCENE']] = float(item['SUCCESS_AMOUNT'])
    return data


def deal_customer(alert_list, CUSTOMER, sale_name, customer_no, stat_dispaysignedname, this_week_data, last_week_data,
                  market_fluctuation):
    for payer_customer_signedname in CUSTOMER['PAYER_CUSTOMER_SIGNEDNAME_list']:
        if payer_customer_signedname not in CUSTOMER['PAYER_CUSTOMER_SIGNEDNAME_to_SUCCESS_AMOUNT_this_week']:
            CUSTOMER['PAYER_CUSTOMER_SIGNEDNAME_to_SUCCESS_AMOUNT_this_week'][payer_customer_signedname] = 0
        if payer_customer_signedname not in CUSTOMER['PAYER_CUSTOMER_SIGNEDNAME_to_SUCCESS_AMOUNT_last_week']:
            CUSTOMER['PAYER_CUSTOMER_SIGNEDNAME_to_SUCCESS_AMOUNT_last_week'][payer_customer_signedname] = 0
    # 警告判断

    # 遍历CUSTOMER
    for payer_customer_signedname in CUSTOMER['PAYER_CUSTOMER_SIGNEDNAME_list']:
        PAYER_CUSTOMER_SIGNEDNAME_to_SUCCESS_AMOUNT_this_week = \
            CUSTOMER['PAYER_CUSTOMER_SIGNEDNAME_to_SUCCESS_AMOUNT_this_week'][payer_customer_signedname]
        PAYER_CUSTOMER_SIGNEDNAME_to_SUCCESS_AMOUNT_last_week = \
            CUSTOMER['PAYER_CUSTOMER_SIGNEDNAME_to_SUCCESS_AMOUNT_last_week'][payer_customer_signedname]
        content = None

        if PAYER_CUSTOMER_SIGNEDNAME_to_SUCCESS_AMOUNT_last_week == 0:
            pass
            # if PAYER_CUSTOMER_SIGNEDNAME_to_SUCCESS_AMOUNT_this_week >= 50 * (10 ** 4):
            #     content = f'付方名称:{payer_customer_signedname}，航司:{stat_dispaysignedname}——商编:{customer_no}+场景字段，近7天充值金额为{PAYER_CUSTOMER_SIGNEDNAME_to_SUCCESS_AMOUNT_this_week}，近7天充值金额为{PAYER_CUSTOMER_SIGNEDNAME_to_SUCCESS_AMOUNT_last_week}'
            #     alert_list.append({'name': sale_name, 'title': '深航/国航充值业务', 'content': content})
        else:
            fluctuation = (PAYER_CUSTOMER_SIGNEDNAME_to_SUCCESS_AMOUNT_this_week /
                           PAYER_CUSTOMER_SIGNEDNAME_to_SUCCESS_AMOUNT_last_week) - (
                                  CUSTOMER['SUCCESS_AMOUNT_this_week'] / CUSTOMER['SUCCESS_AMOUNT_last_week'])
            flag = False
            if PAYER_CUSTOMER_SIGNEDNAME_to_SUCCESS_AMOUNT_this_week >= 1500 * (10 ** 4):
                if fluctuation <= -0.15 or fluctuation >= 0.20:
                    flag = True
            elif PAYER_CUSTOMER_SIGNEDNAME_to_SUCCESS_AMOUNT_this_week < 1500 * (
                    10 ** 4) and PAYER_CUSTOMER_SIGNEDNAME_to_SUCCESS_AMOUNT_this_week >= 100 * (10 ** 4):
                if fluctuation <= -0.50 or fluctuation >= 0.50:
                    flag = True
            elif PAYER_CUSTOMER_SIGNEDNAME_to_SUCCESS_AMOUNT_this_week < 100 * (
                    10 ** 4) and PAYER_CUSTOMER_SIGNEDNAME_to_SUCCESS_AMOUNT_this_week >= 50 * (10 ** 4):
                if fluctuation <= -0.80 or fluctuation >= 0.80:
                    flag = True

            if flag == True:
                success_amount_this_week_by_payer_business_scene = find_by_payer_and_stat_dispaysignedname(
                    this_week_data, customer_no, payer_customer_signedname)
                success_amount_last_week_by_payer_business_scene = find_by_payer_and_stat_dispaysignedname(
                    last_week_data, customer_no, payer_customer_signedname)
                for key, value in success_amount_this_week_by_payer_business_scene.items():
                    if key not in success_amount_last_week_by_payer_business_scene:
                        success_amount_last_week_by_payer_business_scene[key] = 0
                for key, value in success_amount_last_week_by_payer_business_scene.items():
                    if key not in success_amount_this_week_by_payer_business_scene:
                        success_amount_this_week_by_payer_business_scene[key] = 0

                for key, value in success_amount_this_week_by_payer_business_scene.items():
                    fluctuation = (success_amount_this_week_by_payer_business_scene[key] /
                                   success_amount_last_week_by_payer_business_scene[key]) - (
                                          CUSTOMER['SUCCESS_AMOUNT_this_week'] / CUSTOMER['SUCCESS_AMOUNT_last_week'])
                    content = f'付方名称:{payer_customer_signedname}，航司:{stat_dispaysignedname}——商编:{customer_no}+场景字段:{key}，近7天充值金额，环比上周{"上升" if fluctuation > 0 else "下降"}{abs(fluctuation * 100):.2f}%，{"高于" if market_fluctuation > 0 else "低于"}大盘{abs(market_fluctuation*10):.2f}%'
                    subcontent = f'近7天充值金额，环比上周{"上升" if fluctuation > 0 else "下降"}{abs(fluctuation * 100):.2f}%，{"高于" if market_fluctuation > 0 else "低于"}大盘{abs(market_fluctuation*10):.2f}%'
                    alert_list.append({
                        'name': sale_name,
                        'title': '深航/国航充值业务',
                        'content': content,
                        'payer_customer_signedname': payer_customer_signedname,
                        'stat_dispaysignedname': stat_dispaysignedname,
                        'customer_no': customer_no,
                        'payer_business_scene': key,
                        'sub_content': subcontent,
                    })

    return alert_list


def monitor4():
    try:
        print('开始获取监控四所需数据')
        this_week_data = monitor4_data.get_this_week_data_in_monitor4()
        last_week_data = monitor4_data.get_last_week_data_in_monitor4()
        sale_name1 = monitor4_data.search_by_customer_no('10012407595')[0]['SALES_NAME']
        sale_name2 = monitor4_data.search_by_customer_no('10034228238')[0]['SALES_NAME']
        total_success_amount_this_week = float(monitor4_data.get_total_success_amount_this_week())
        total_success_amount_last_week = float(monitor4_data.get_total_success_amount_last_week())
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
            if item['PAYER_CUSTOMER_SIGNEDNAME'] in CUSTOMER1['PAYER_CUSTOMER_SIGNEDNAME_to_SUCCESS_AMOUNT_this_week']:
                CUSTOMER1['PAYER_CUSTOMER_SIGNEDNAME_to_SUCCESS_AMOUNT_this_week'][
                    item['PAYER_CUSTOMER_SIGNEDNAME']] += float(item['SUCCESS_AMOUNT'])
            else:
                CUSTOMER1['PAYER_CUSTOMER_SIGNEDNAME_to_SUCCESS_AMOUNT_this_week'][
                    item['PAYER_CUSTOMER_SIGNEDNAME']] = float(item['SUCCESS_AMOUNT'])
        elif item['CUSTOMER_NO'] == '10034228238':
            CUSTOMER2['PAYER_CUSTOMER_SIGNEDNAME_list'].add(item['PAYER_CUSTOMER_SIGNEDNAME'])
            CUSTOMER2['SUCCESS_AMOUNT_this_week'] += float(item['SUCCESS_AMOUNT'])
            if item['PAYER_CUSTOMER_SIGNEDNAME'] in CUSTOMER2['PAYER_CUSTOMER_SIGNEDNAME_to_SUCCESS_AMOUNT_this_week']:
                CUSTOMER2['PAYER_CUSTOMER_SIGNEDNAME_to_SUCCESS_AMOUNT_this_week'][
                    item['PAYER_CUSTOMER_SIGNEDNAME']] += float(item['SUCCESS_AMOUNT'])
            else:
                CUSTOMER2['PAYER_CUSTOMER_SIGNEDNAME_to_SUCCESS_AMOUNT_this_week'][
                    item['PAYER_CUSTOMER_SIGNEDNAME']] = float(item['SUCCESS_AMOUNT'])

    for item in last_week_data:
        if item['CUSTOMER_NO'] == '10012407595':
            CUSTOMER1['PAYER_CUSTOMER_SIGNEDNAME_list'].add(item['PAYER_CUSTOMER_SIGNEDNAME'])
            CUSTOMER1['SUCCESS_AMOUNT_last_week'] += float(item['SUCCESS_AMOUNT'])
            if item['PAYER_CUSTOMER_SIGNEDNAME'] in CUSTOMER1['PAYER_CUSTOMER_SIGNEDNAME_to_SUCCESS_AMOUNT_last_week']:
                CUSTOMER1['PAYER_CUSTOMER_SIGNEDNAME_to_SUCCESS_AMOUNT_last_week'][
                    item['PAYER_CUSTOMER_SIGNEDNAME']] += float(item['SUCCESS_AMOUNT'])
            else:
                CUSTOMER1['PAYER_CUSTOMER_SIGNEDNAME_to_SUCCESS_AMOUNT_last_week'][
                    item['PAYER_CUSTOMER_SIGNEDNAME']] = float(item['SUCCESS_AMOUNT'])
        elif item['CUSTOMER_NO'] == '10034228238':
            CUSTOMER2['PAYER_CUSTOMER_SIGNEDNAME_list'].add(item['PAYER_CUSTOMER_SIGNEDNAME'])
            CUSTOMER2['SUCCESS_AMOUNT_last_week'] += float(item['SUCCESS_AMOUNT'])
            if item['PAYER_CUSTOMER_SIGNEDNAME'] in CUSTOMER2['PAYER_CUSTOMER_SIGNEDNAME_to_SUCCESS_AMOUNT_last_week']:
                CUSTOMER2['PAYER_CUSTOMER_SIGNEDNAME_to_SUCCESS_AMOUNT_last_week'][
                    item['PAYER_CUSTOMER_SIGNEDNAME']] += float(item['SUCCESS_AMOUNT'])
            else:
                CUSTOMER2['PAYER_CUSTOMER_SIGNEDNAME_to_SUCCESS_AMOUNT_last_week'][
                    item['PAYER_CUSTOMER_SIGNEDNAME']] = float(item['SUCCESS_AMOUNT'])

    print('监控四开始判断预警')
    market_fluctuation = total_success_amount_this_week/total_success_amount_last_week - 1
    alert_list = []
    alert_list = deal_customer(alert_list, CUSTOMER1, sale_name1, customer_no1, stat_dispaysignedname1, this_week_data,
                               last_week_data, market_fluctuation)
    alert_list = deal_customer(alert_list, CUSTOMER2, sale_name2, customer_no2, stat_dispaysignedname2, this_week_data,
                               last_week_data, market_fluctuation)

    return alert_list

# a = monitor4()
# print(a)