from dbgpt.extra.dag.buildin_awel.monitor import monitor3_data
from dbgpt.extra.dag.buildin_awel.monitor.api import get_past_working_days


class Monitor3:
    def __init__(self):
        self.alert_list = []
        try:
            print('监控二中开始获取工作日')
            self.d_1_trx_date = ','.join(get_past_working_days(1))
            self.d_2_trx_date = ','.join(get_past_working_days(2)).split(',')[1]
        except Exception as e:
            raise e

    def run(self):
        self.run_by_stat()
        self.run_by_payer()
        return self.alert_list

    def run_by_stat(self):
        print('监控三(商户签约名维度)开始执行')
        sales_name_list = set()
        try:
            print('监控三开始获取所有销售')
            d_1_data = monitor3_data.get_data_by_stat_in_monitor3(self.d_1_trx_date)
            d_2_data = monitor3_data.get_data_by_stat_in_monitor3(self.d_2_trx_date)
            for item in d_1_data:
                sales_name_list.add(item['SALES_NAME'])
            for item in d_2_data:
                sales_name_list.add(item['SALES_NAME'])
        except Exception as e:
            print('监控三开始获取所有销售失败')

        for sales_name in sales_name_list:
            self.deal_sales_name(sales_name)

    def deal_sales_name(self, sales_name):
        customer_list = set()
        d_1_customer_to_success_amount = {}
        d_2_customer_to_success_amount = {}
        try:
            print(f'监控三开始获取{sales_name}的商户签约名')
            d_1_data = monitor3_data.get_data_by_stat_in_monitor3(trx_date=self.d_1_trx_date, sales_name=sales_name)
            d_2_data = monitor3_data.get_data_by_stat_in_monitor3(trx_date=self.d_2_trx_date, sales_name=sales_name)
            for item in d_1_data:
                customer_list.add(item['STAT_DISPAYSIGNEDNAME'])
                d_1_customer_to_success_amount[item['STAT_DISPAYSIGNEDNAME']] = float(item['SUCCESS_AMOUNT'])
            for item in d_2_data:
                customer_list.add(item['STAT_DISPAYSIGNEDNAME'])
                d_2_customer_to_success_amount[item['STAT_DISPAYSIGNEDNAME']] = float(item['SUCCESS_AMOUNT'])
        except Exception as e:
            print(f'监控三开始获取{sales_name}的商户签约名失败！')
            return

        for customer in customer_list:
            d_1_customer_success_amount = 0
            d_2_customer_success_amount = 0
            if customer in d_1_customer_to_success_amount:
                d_1_customer_success_amount = d_1_customer_to_success_amount[customer]
            if customer in d_2_customer_to_success_amount:
                d_2_customer_success_amount = d_2_customer_to_success_amount[customer]
            # 除数为0，抛弃
            if d_1_customer_success_amount == 0 or d_2_customer_success_amount == 0:
                continue
            self.deal_customer(sales_name, customer, d_1_customer_success_amount, d_2_customer_success_amount)

    def deal_customer(self, sales_name, customer, d_1_customer_success_amount:float, d_2_customer_success_amount:float):
        product_list = set()
        try:
            print(f'监控三开始获取{sales_name}的商户签约名为{customer}的数据')
            d_1_data = monitor3_data.get_data_by_stat_in_monitor3(trx_date=self.d_1_trx_date, sales_name=sales_name,
                                                                    stat_dispaysignedname=customer)
            d_2_data = monitor3_data.get_data_by_stat_in_monitor3(trx_date=self.d_2_trx_date, sales_name=sales_name,
                                                                    stat_dispaysignedname=customer)

            for item in d_1_data:
                product_list.add(item['PRODUCT'])
            for item in d_2_data:
                product_list.add(item['PRODUCT'])

        except Exception as e:
            print(f'监控三开始获取{sales_name}的商户签约名为{customer}的数据失败')
            return

        for product in product_list:
            self.deal_product(sales_name, customer, d_1_customer_success_amount, d_2_customer_success_amount, product)

    def deal_product(self, sales_name, customer, d_1_customer_success_amount, d_2_customer_success_amount, product):
        try:
            print(f'监控三开始获取{sales_name}的商户 签约名为{customer}的数据')
            d_1_data = monitor3_data.get_data_by_stat_in_monitor3(trx_date=self.d_1_trx_date, sales_name=sales_name,
                                                                    stat_dispaysignedname=customer, product=product)
            d_2_data = monitor3_data.get_data_by_stat_in_monitor3(trx_date=self.d_2_trx_date, sales_name=sales_name,
                                                                  stat_dispaysignedname=customer, product=product)
        except Exception as e:
            print(f'监控三开始获取{sales_name}的商户签约名为{customer}的数据失败')
            return

        try:
            '''
            A：【产品交易金额占比的环比差值】的绝对值>60%
            【产品交易金额占比的环比差值】（[D-1]商户各产品交易金额 / [D-1]商户交易金额）-（[D-2]商户各产品交易金额 / [D-2]商户交易金额）
            B：([D-1]产品交易金额- [D-2]产品交易金额）的绝对值>=100000
            '''
            print(f'监控三开始处理{sales_name}的商户签约名为{customer}的产品为{product}数据')
            d_1_product_success_amount = 0
            d_2_product_success_amount = 0
            if len(d_1_data) > 0:
                d_1_product_success_amount = float(d_1_data[0]['SUCCESS_AMOUNT'])
            if len(d_2_data) > 0:
                d_2_product_success_amount = float(d_2_data[0]['SUCCESS_AMOUNT'])

            difference = (d_1_product_success_amount/d_1_customer_success_amount) - (d_2_product_success_amount/d_2_customer_success_amount)
            if difference > 0.6 and abs(d_1_product_success_amount-d_2_product_success_amount) > 100000:
                self.alert_list.append({
                    'name': sales_name,
                    'title': '商户（收方或付方）产品波动异常',
                    'customer_name': customer,
                    'content': f'交易无明显波动，但{product}产品结构有变化，变化值为{difference*100:.2f}%，请关注。',
                    'content_rich': f"波动详情：      交易无明显波动，但{product}产品结构有变化，变化值为<text_tag color={'orange' if difference < 1 else 'carmine'}>{difference * 100:.2f}%</text_tag>，请关注。",
                    "type": "商户签约名"

                })
        except Exception as e:
            print(f'监控三开始处理{sales_name}的商户签约名为{customer}的产品为{product}数据失败')



    def run_by_payer(self):
        print('监控三(付方签约名维度)开始执行')
        payer_sales_name_list = set()
        try:
            print('监控三开始获取所有付方销售')
            d_1_data = monitor3_data.get_data_by_payer_in_monitor3(self.d_1_trx_date)
            d_2_data = monitor3_data.get_data_by_payer_in_monitor3(self.d_2_trx_date)
            for item in d_1_data:
                payer_sales_name_list.add(item['PAYER_SALES_NAME'])
            for item in d_2_data:
                payer_sales_name_list.add(item['PAYER_SALES_NAME'])
        except Exception as e:
            print('监控三开始获取所有付方销售失败')

        for payer_sales_name in payer_sales_name_list:
            self.deal_payer_sales_name(payer_sales_name)

    def deal_payer_sales_name(self, payer_sales_name):
        payer_customer_list = set()
        d_1_payer_customer_to_success_amount = {}
        d_2_payer_customer_to_success_amount = {}
        try:
            print(f'监控三开始获取{payer_sales_name}的付方签约名')
            d_1_data = monitor3_data.get_data_by_payer_in_monitor3(trx_date=self.d_1_trx_date, payer_sales_name=payer_sales_name)
            d_2_data = monitor3_data.get_data_by_payer_in_monitor3(trx_date=self.d_2_trx_date, payer_sales_name=payer_sales_name)
            for item in d_1_data:
                payer_customer_list.add(item['PAYER_CUSTOMER_SIGNEDNAME'])
                d_1_payer_customer_to_success_amount[item['PAYER_CUSTOMER_SIGNEDNAME']] = float(item['SUCCESS_AMOUNT'])
            for item in d_2_data:
                payer_customer_list.add(item['PAYER_CUSTOMER_SIGNEDNAME'])
                d_2_payer_customer_to_success_amount[item['PAYER_CUSTOMER_SIGNEDNAME']] = float(item['SUCCESS_AMOUNT'])
        except Exception as e:
            print(f'监控三开始获取{payer_sales_name}的付方签约名失败！')
            return

        for payer_customer in payer_customer_list:
            d_1_payer_customer_success_amount = 0
            d_2_payer_customer_success_amount = 0
            if payer_customer in d_1_payer_customer_to_success_amount:
                d_1_payer_customer_success_amount = d_1_payer_customer_to_success_amount[payer_customer]
            if payer_customer in d_2_payer_customer_to_success_amount:
                d_2_payer_customer_success_amount = d_2_payer_customer_to_success_amount[payer_customer]
            # 除数为0，抛弃
            if d_1_payer_customer_success_amount == 0 or d_2_payer_customer_success_amount == 0:
                continue
            self.deal_payer_customer(payer_sales_name, payer_customer, d_1_payer_customer_success_amount, d_2_payer_customer_success_amount)

    def deal_payer_customer(self, payer_sales_name, payer_customer, d_1_payer_customer_success_amount: float,
                      d_2_payer_customer_success_amount: float):
        payer_product_list = set()
        try:
            print(f'监控三开始获取{payer_sales_name}的付方签约名为{payer_customer}的数据')
            d_1_data = monitor3_data.get_data_by_payer_in_monitor3(trx_date=self.d_1_trx_date, payer_sales_name=payer_sales_name,
                                                                  payer_customer_signedname=payer_customer)
            d_2_data = monitor3_data.get_data_by_payer_in_monitor3(trx_date=self.d_2_trx_date, payer_sales_name=payer_sales_name,
                                                                  payer_customer_signedname=payer_customer)

            for item in d_1_data:
                payer_product_list.add(item['PRODUCT'])
            for item in d_2_data:
                payer_product_list.add(item['PRODUCT'])

        except Exception as e:
            print(f'监控三开始获取{payer_sales_name}的付方签约名为{payer_customer}的数据失败')
            return

        for payer_product in payer_product_list:
            self.deal_payer_product(payer_sales_name, payer_customer, d_1_payer_customer_success_amount, d_2_payer_customer_success_amount, payer_product)

    def deal_payer_product(self, payer_sales_name, payer_customer, d_1_payer_customer_success_amount, d_2_payer_customer_success_amount, payer_product):
        try:
            print(f'监控三开始获取{payer_sales_name}的付方签约名为{payer_customer}的数据')
            d_1_data = monitor3_data.get_data_by_payer_in_monitor3(trx_date=self.d_1_trx_date, payer_sales_name=payer_sales_name,
                                                                    payer_customer_signedname=payer_customer, product=payer_product)
            d_2_data = monitor3_data.get_data_by_payer_in_monitor3(trx_date=self.d_2_trx_date, payer_sales_name=payer_sales_name,
                                                                  payer_customer_signedname=payer_customer, product=payer_product)
        except Exception as e:
            print(f'监控三开始获取{payer_sales_name}的付方签约名为{payer_customer}的数据失败')
            return

        try:
            '''
            A：【产品交易金额占比的环比差值】的绝对值>60%
            【产品交易金额占比的环比差值】（[D-1]商户各产品交易金额 / [D-1]商户交易金额）-（[D-2]商户各产品交易金额 / [D-2]商户交易金额）
            B：([D-1]产品交易金额- [D-2]产品交易金额）的绝对值>=100000
            '''
            print(f'监控三开始处理{payer_customer}的付方签约名为{payer_customer}的产品为{payer_product}数据')
            d_1_payer_product_success_amount = 0
            d_2_payer_product_success_amount = 0
            if len(d_1_data) > 0:
                d_1_payer_product_success_amount = float(d_1_data[0]['SUCCESS_AMOUNT'])
            if len(d_2_data) > 0:
                d_2_payer_product_success_amount = float(d_2_data[0]['SUCCESS_AMOUNT'])

            difference = (d_1_payer_product_success_amount/d_1_payer_customer_success_amount) - (d_2_payer_product_success_amount/d_2_payer_customer_success_amount)
            if difference > 0.6 and abs(d_1_payer_product_success_amount-d_2_payer_product_success_amount) > 100000:
                self.alert_list.append({
                    'name': payer_sales_name,
                    'title': '商户（收方或付方）产品波动异常',
                    'customer_name': payer_customer,
                    'content': f'交易无明显波动，但{payer_product}产品结构有变化，变化值为{difference*100:.2f}%，请关注。',
                    'content_rich': f"波动详情：      交易无明显波动，但{payer_product}产品结构有变化，变化值为<text_tag color={'orange' if difference < 1 else 'carmine'}>{difference * 100:.2f}%</text_tag>，请关注。",
                    "type": "付方签约名"
                })
        except Exception as e:
            print(f'监控三开始处理{payer_sales_name}的付方签约名为{payer_customer}的产品为{payer_product}数据失败')

