from collections import defaultdict
from typing import Dict

from dbgpt.extra.dag.buildin_awel.monitor.airline_monitor_handler import AirlineMonitorDataHandler


class Monitor3(AirlineMonitorDataHandler):
    def __init__(self):
        super().__init__()
        self.alert_list = []

    def prepare_data(self):
        self.alert_list = []
        try:
            print('监控三中开始获取工作日')
            self.d_1_trx_date = ','.join(self.get_past_working_days(1))
            self.d_2_trx_date = ','.join(self.get_past_working_days(2)).split(',')[1]
        except Exception as e:
            raise e

    def run(self):
        self.prepare_data()
        self.run_by_stat()
        self.run_by_payer()
        def custom_sort(data):
            return (data['data']['type'], data['data']['sales_name'], -data['data']['proportion_value'])

        self.alert_list = sorted(self.alert_list, key=custom_sort)
        return self.alert_list

    def run_by_stat(self):
        print('监控三(商户签约名维度)开始执行')
        sales_name_list = set()
        try:
            print('监控三开始获取所有销售')
            d_1_data = self.monitor3_data.get_data_by_stat_in_monitor3(self.d_1_trx_date)
            d_2_data = self.monitor3_data.get_data_by_stat_in_monitor3(self.d_2_trx_date)
            for item in d_1_data:
                sales_name_list.add(item['SALES_NAME'])
            for item in d_2_data:
                sales_name_list.add(item['SALES_NAME'])
        except Exception as e:
            print('监控三开始获取所有销售失败')

        d1_result_sales, d1_result_sales_custom, d1_result_sales_custom_produc = self.build_d_n_stat_datas_by_some("d1")
        d2_result_sales, d2_result_sales_custom, d2_result_sales_custom_produc = self.build_d_n_stat_datas_by_some("d2")

        for sales_name in sales_name_list:
            self.deal_sales_name(
                d1_result_sales,
                d1_result_sales_custom,
                d1_result_sales_custom_produc,
                d2_result_sales,
                d2_result_sales_custom,
                d2_result_sales_custom_produc,
                sales_name
            )

    def build_d_n_stat_datas_by_some(self, days_type):
        """按1、销售，2、销售、签约名，3、销售、签约名、产品分组，构造数据"""
        d_n_datas = []
        if days_type == "d1":
            d_n_datas = self.monitor3_data.get_data_by_stat_in_monitor3(
                trx_date=self.d_1_trx_date
            )
        if days_type == "d2":
            d_n_datas = self.monitor3_data.get_data_by_stat_in_monitor3(
                trx_date=self.d_2_trx_date
            )
        for rec in d_n_datas:
            if rec["SALES_NAME"] is None:
                rec["SALES_NAME"] = "None"
            if rec["STAT_DISPAYSIGNEDNAME"] is None:
                rec["STAT_DISPAYSIGNEDNAME"] = "None"
            if rec["PRODUCT"] is None:
                rec["PRODUCT"] = "None"
        print(f'监控三({days_type})构造条数: {len(d_n_datas)}！')

        result_sales = defaultdict(list)
        result_sales_custom = defaultdict(list)
        result_sales_custom_produc = defaultdict(list)
        for rec in d_n_datas:
            result_sales[rec["SALES_NAME"]].append(rec)
        for rec in d_n_datas:
            k = str(rec["SALES_NAME"]) + '#_#' + str(rec["STAT_DISPAYSIGNEDNAME"])
            result_sales_custom[k].append(rec)
        for rec in d_n_datas:
            k = str(rec["SALES_NAME"]) + '#_#' + str(rec["STAT_DISPAYSIGNEDNAME"]) + '#_#' + str(rec["PRODUCT"])
            result_sales_custom_produc[k].append(rec)
        return result_sales, result_sales_custom, result_sales_custom_produc

    def build_d_n_payer_datas_by_some(self, days_type):
        """按1、销售，2、销售、签约名，3、销售、签约名、产品分组，构造数据"""
        d_n_datas = []
        if days_type == "d1":
            d_n_datas = self.monitor3_data.get_data_by_payer_in_monitor3(
                trx_date=self.d_1_trx_date
            )
        if days_type == "d2":
            d_n_datas = self.monitor3_data.get_data_by_payer_in_monitor3(
                trx_date=self.d_2_trx_date
            )
        print(f'监控三({days_type})构造条数: {len(d_n_datas)}！')

        for rec in d_n_datas:
            if rec["PAYER_SALES_NAME"] is None:
                rec["PAYER_SALES_NAME"] = "None"
            if rec["PAYER_DISPAYSIGNEDNAME"] is None:
                rec["PAYER_DISPAYSIGNEDNAME"] = "None"
            if rec["PRODUCT"] is None:
                rec["PRODUCT"] = "None"
        result_sales = defaultdict(list)
        result_sales_custom = defaultdict(list)
        result_sales_custom_produc = defaultdict(list)
        for rec in d_n_datas:
            result_sales[rec["PAYER_SALES_NAME"]].append(rec)
        for rec in d_n_datas:
            k = str(rec["PAYER_SALES_NAME"]) + '#_#' + str(rec["PAYER_DISPAYSIGNEDNAME"])
            result_sales_custom[k].append(rec)
        for rec in d_n_datas:
            k = str(rec["PAYER_SALES_NAME"]) + '#_#' + str(rec["PAYER_DISPAYSIGNEDNAME"]) + '#_#' + str(
                rec["PRODUCT"])
            result_sales_custom_produc[k].append(rec)
        return result_sales, result_sales_custom, result_sales_custom_produc

    def deal_sales_name(
            self,
            d1_result_sales,
            d1_result_sales_custom,
            d1_result_sales_custom_produc,
            d2_result_sales,
            d2_result_sales_custom,
            d2_result_sales_custom_produc,
            sales_name
    ):
        customer_list = set()
        d_1_customer_to_success_amount = {}
        d_2_customer_to_success_amount = {}
        try:
            print(f'监控三开始获取{sales_name}的商户签约名')

            d_1_data = d1_result_sales[sales_name]
            d_2_data = d2_result_sales[sales_name]

            # d_1_data = self.monitor3_data.get_data_by_stat_in_monitor3(
            #     trx_date=self.d_1_trx_date,
            #     sales_name=sales_name
            # )
            # d_2_data = self.monitor3_data.get_data_by_stat_in_monitor3(
            #     trx_date=self.d_2_trx_date,
            #     sales_name=sales_name
            # )
            for item in d_1_data:
                customer_list.add(item['STAT_DISPAYSIGNEDNAME'])
                if item['STAT_DISPAYSIGNEDNAME'] not in d_1_customer_to_success_amount:
                    d_1_customer_to_success_amount[item['STAT_DISPAYSIGNEDNAME']] = 0
                d_1_customer_to_success_amount[item['STAT_DISPAYSIGNEDNAME']] += float(item['SUCCESS_AMOUNT'])
            for item in d_2_data:
                customer_list.add(item['STAT_DISPAYSIGNEDNAME'])
                if item['STAT_DISPAYSIGNEDNAME'] not in d_2_customer_to_success_amount:
                    d_2_customer_to_success_amount[item['STAT_DISPAYSIGNEDNAME']] = 0
                d_2_customer_to_success_amount[item['STAT_DISPAYSIGNEDNAME']] += float(item['SUCCESS_AMOUNT'])
            print(f'监控三开始获取{sales_name}的商户签约名成功！')

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
            self.deal_customer(
                d1_result_sales_custom,
                d1_result_sales_custom_produc,
                d2_result_sales_custom,
                d2_result_sales_custom_produc,
                sales_name,
                customer,
                d_1_customer_success_amount,
                d_2_customer_success_amount
            )

    def deal_customer(
            self,
            d1_result_sales_custom,
            d1_result_sales_custom_produc,
            d2_result_sales_custom,
            d2_result_sales_custom_produc,
            sales_name, customer, d_1_customer_success_amount: float,
            d_2_customer_success_amount: float
    ):
        product_list = set()
        try:
            print(f'监控三开始获取{sales_name}的商户签约名为{customer}的数据')
            d_1_data = d1_result_sales_custom[sales_name + "#_#" + customer]
            d_2_data = d2_result_sales_custom[sales_name + "#_#" + customer]
            # d_1_data = self.monitor3_data.get_data_by_stat_in_monitor3(
            #     trx_date=self.d_1_trx_date,
            #     sales_name=sales_name,
            #     stat_dispaysignedname=customer
            # )
            # d_2_data = self.monitor3_data.get_data_by_stat_in_monitor3(
            #     trx_date=self.d_2_trx_date,
            #     sales_name=sales_name,
            #     stat_dispaysignedname=customer
            # )

            for item in d_1_data:
                product_list.add(item['PRODUCT'])
            for item in d_2_data:
                product_list.add(item['PRODUCT'])
            print(f'监控三开始获取{sales_name}的商户签约名为{customer}的数据成功')
        except Exception as e:
            print(f'监控三开始获取{sales_name}的商户签约名为{customer}的数据失败')
            return

        for product in product_list:
            self.deal_product(d1_result_sales_custom_produc, d2_result_sales_custom_produc, sales_name, customer,
                              d_1_customer_success_amount, d_2_customer_success_amount, product)

    def deal_product(self, d1_result_sales_custom_produc, d2_result_sales_custom_produc, sales_name, customer,
                     d_1_customer_success_amount, d_2_customer_success_amount, product):
        try:
            print(f'监控三开始获取{sales_name}的商户 签约名为{customer}的数据')
            d_1_data = d1_result_sales_custom_produc[sales_name + "#_#" + customer + "#_#" + product]
            d_2_data = d2_result_sales_custom_produc[sales_name + "#_#" + customer + "#_#" + product]

            # d_1_data = self.monitor3_data.get_data_by_stat_in_monitor3(
            #     trx_date=self.d_1_trx_date,
            #     sales_name=sales_name,
            #     stat_dispaysignedname=customer,
            #     product=product
            # )
            # d_2_data = self.monitor3_data.get_data_by_stat_in_monitor3(
            #     trx_date=self.d_2_trx_date,
            #     sales_name=sales_name,
            #     stat_dispaysignedname=customer,
            #     product=product
            # )
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

            difference = (d_1_product_success_amount / d_1_customer_success_amount) - (
                    d_2_product_success_amount / d_2_customer_success_amount)
            if abs(difference) > 0.6 and abs(d_1_product_success_amount - d_2_product_success_amount) > 100000:
                self.alert_list.append({
                    'name': sales_name,
                    'title': '商户（收方或付方）产品波动异常',
                    'customer_name': f'<font color=green>{customer}</font>',
                    'customer_name_text': customer,
                    'content': f'交易无明显波动，但{product}产品结构有变化，变化值为{difference * 100:.2f}%，请关注。',
                    'content_rich': f"交易无明显波动，但{product}产品结构有变化，变化值为**<font color={'orange' if difference < 1 else 'carmine'}>{difference * 100:.2f}%</font>**，请关注。",
                    'type': f'<font color=green>收方</font>',
                    'type_text': '收方',
                    'data':{
                        'monitor_type': '3',
                        'type': '收方',
                        'customer_name': customer,
                        'sales_name': sales_name,
                        'product': product,
                        'd_1_product_success_amount': d_1_product_success_amount,
                        'd_2_product_success_amount': d_2_product_success_amount,
                        'd_2_customer_success_amount': d_2_customer_success_amount,
                        'd_1_customer_success_amount': d_1_customer_success_amount,
                        'proportion_value': difference,
                        'remarks': '收方还是付方是type，签约名是customer_name，销售名是sales_name，产品名是product，变化值是proportion_value'
                    }
                })
        except Exception as e:
            print(f'监控三开始处理{sales_name}的商户签约名为{customer}的产品为{product}数据失败')

    def run_by_payer(self):
        print('监控三(付方签约名维度)开始执行')
        payer_sales_name_list = set()

        try:
            print('监控三开始获取所有付方销售')
            d_1_data = self.monitor3_data.get_data_by_payer_in_monitor3(self.d_1_trx_date)
            d_2_data = self.monitor3_data.get_data_by_payer_in_monitor3(self.d_2_trx_date)

            for item in d_1_data:
                payer_sales_name_list.add(item['PAYER_SALES_NAME'])
            for item in d_2_data:
                payer_sales_name_list.add(item['PAYER_SALES_NAME'])

            print('监控三开始获取所有付方销售成功')
        except Exception as e:
            print('监控三开始获取所有付方销售失败')

        d1_result_sales, d1_result_sales_custom, d1_result_sales_custom_produc = self.build_d_n_payer_datas_by_some(
            days_type="d1"
        )
        d2_result_sales, d2_result_sales_custom, d2_result_sales_custom_produc = self.build_d_n_payer_datas_by_some(
            days_type="d2"
        )

        for payer_sales_name in payer_sales_name_list:
            self.deal_payer_sales_name(
                d1_result_sales=d1_result_sales,
                d1_result_sales_custom=d1_result_sales_custom,
                d1_result_sales_custom_produc=d1_result_sales_custom_produc,
                d2_result_sales=d2_result_sales,
                d2_result_sales_custom=d2_result_sales_custom,
                d2_result_sales_custom_produc=d2_result_sales_custom_produc,
                payer_sales_name=payer_sales_name
            )

    def deal_payer_sales_name(
            self,
            d1_result_sales,
            d1_result_sales_custom,
            d1_result_sales_custom_produc,
            d2_result_sales,
            d2_result_sales_custom,
            d2_result_sales_custom_produc,
            payer_sales_name
    ):
        payer_customer_list = set()
        d_1_payer_customer_to_success_amount = {}
        d_2_payer_customer_to_success_amount = {}
        try:
            print(f'监控三开始获取{payer_sales_name}的付方签约名')
            d_1_data = d1_result_sales[payer_sales_name]
            d_2_data = d2_result_sales[payer_sales_name]
            # d_1_data = self.monitor3_data.get_data_by_payer_in_monitor3(
            #     trx_date=self.d_1_trx_date,
            #     payer_sales_name=payer_sales_name
            # )
            # d_2_data = self.monitor3_data.get_data_by_payer_in_monitor3(
            #     trx_date=self.d_2_trx_date,
            #     payer_sales_name=payer_sales_name
            # )
            for item in d_1_data:
                payer_customer_list.add(item['PAYER_DISPAYSIGNEDNAME'])
                if item['PAYER_DISPAYSIGNEDNAME'] not in d_1_payer_customer_to_success_amount:
                    d_1_payer_customer_to_success_amount[item['PAYER_DISPAYSIGNEDNAME']] = 0
                d_1_payer_customer_to_success_amount[item['PAYER_DISPAYSIGNEDNAME']] += float(item['SUCCESS_AMOUNT'])
            for item in d_2_data:
                payer_customer_list.add(item['PAYER_DISPAYSIGNEDNAME'])
                if item['PAYER_DISPAYSIGNEDNAME'] not in d_2_payer_customer_to_success_amount:
                    d_2_payer_customer_to_success_amount[item['PAYER_DISPAYSIGNEDNAME']] = 0
                d_2_payer_customer_to_success_amount[item['PAYER_DISPAYSIGNEDNAME']] += float(item['SUCCESS_AMOUNT'])

            print(f'监控三开始获取{payer_sales_name}的付方签约名成功！')
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
            self.deal_payer_customer(
                d1_result_sales_custom,
                d1_result_sales_custom_produc,
                d2_result_sales_custom,
                d2_result_sales_custom_produc,
                payer_sales_name,
                payer_customer,
                d_1_payer_customer_success_amount,
                d_2_payer_customer_success_amount
            )

    def deal_payer_customer(
            self,
            d1_result_sales_custom,
            d1_result_sales_custom_produc,
            d2_result_sales_custom,
            d2_result_sales_custom_produc,
            payer_sales_name,
            payer_customer,
            d_1_payer_customer_success_amount: float,
            d_2_payer_customer_success_amount: float):
        payer_product_list = set()
        try:
            print(f'监控三开始获取{payer_sales_name}的付方签约名为{payer_customer}的数据')
            d_1_data = d1_result_sales_custom[payer_sales_name + "#_#" + payer_customer]
            d_2_data = d2_result_sales_custom[payer_sales_name + "#_#" + payer_customer]
            # d_1_data = self.monitor3_data.get_data_by_payer_in_monitor3(
            #     trx_date=self.d_1_trx_date,
            #     payer_sales_name=payer_sales_name,
            #     payer_customer_signedname=payer_customer
            # )
            # d_2_data = self.monitor3_data.get_data_by_payer_in_monitor3(
            #     trx_date=self.d_2_trx_date,
            #     payer_sales_name=payer_sales_name,
            #     payer_customer_signedname=payer_customer
            # )

            for item in d_1_data:
                payer_product_list.add(item['PRODUCT'])
            for item in d_2_data:
                payer_product_list.add(item['PRODUCT'])
            print(f'监控三开始获取{payer_sales_name}的付方签约名为{payer_customer}的数据成功')
        except Exception as e:
            print(f'监控三开始获取{payer_sales_name}的付方签约名为{payer_customer}的数据失败')
            return

        for payer_product in payer_product_list:
            self.deal_payer_product(
                d1_result_sales_custom_produc,
                d2_result_sales_custom_produc,
                payer_sales_name,
                payer_customer,
                d_1_payer_customer_success_amount,
                d_2_payer_customer_success_amount,
                payer_product
            )

    def deal_payer_product(
            self,
            d1_result_sales_custom_produc,
            d2_result_sales_custom_produc,
            payer_sales_name, payer_customer,
            d_1_payer_customer_success_amount,
            d_2_payer_customer_success_amount,
            payer_product
    ):
        try:
            print(f'监控三开始获取{payer_sales_name}的付方签约名为{payer_customer}的数据')
            d_1_data = d1_result_sales_custom_produc[payer_sales_name + "#_#" + payer_customer + "#_#" + payer_product]
            d_2_data = d2_result_sales_custom_produc[payer_sales_name + "#_#" + payer_customer + "#_#" + payer_product]
            # d_1_data = self.monitor3_data.get_data_by_payer_in_monitor3(
            #     trx_date=self.d_1_trx_date,
            #     payer_sales_name=payer_sales_name,
            #     payer_customer_signedname=payer_customer,
            #     product=payer_product
            # )
            # d_2_data = self.monitor3_data.get_data_by_payer_in_monitor3(
            #     trx_date=self.d_2_trx_date,
            #     payer_sales_name=payer_sales_name,
            #     payer_customer_signedname=payer_customer,
            #     product=payer_product
            # )
            print(f'监控三开始获取{payer_sales_name}的付方签约名为{payer_customer}的数据成功')
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

            difference = (d_1_payer_product_success_amount / d_1_payer_customer_success_amount) - (
                    d_2_payer_product_success_amount / d_1_payer_customer_success_amount)
            if abs(difference) > 0.6 and abs(d_1_payer_product_success_amount - d_2_payer_product_success_amount) > 100000:
                self.alert_list.append({
                    'name': payer_sales_name,
                    'title': '商户（收方或付方）产品波动异常',
                    'customer_name': f'<font color=green>{payer_customer}</font>',
                    'customer_name_text': payer_customer,
                    'content': f'交易无明显波动，但{payer_product}产品结构有变化，变化值为{difference * 100:.2f}%，请关注。',
                    'content_rich': f"交易无明显波动，但{payer_product}产品结构有变化，变化值为**<font color={'orange' if difference < 1 else 'carmine'}>{difference * 100:.2f}%</font>**，请关注。",

                    'type': f'<font color=green>付方</font>',
                    'type_text': '付方',
                    'data': {
                        'monitor_type': '3',
                        'type': '付方',
                        'customer_name': payer_customer,
                        'sales_name': payer_sales_name,
                        'product': payer_product,
                        'd_1_product_success_amount': d_1_payer_product_success_amount,
                        'd_2_product_success_amount': d_2_payer_product_success_amount,

                        'd_2_customer_success_amount': d_1_payer_customer_success_amount,
                        'd_1_customer_success_amount': d_1_payer_customer_success_amount,
                        'proportion_value': difference,
                        'remarks': '收方还是付方是type，签约名是customer_name，销售名是sales_name，产品名是product，变化值是proportion_value'
                    }

                })

            print(f'监控三开始处理{payer_sales_name}的付方签约名为{payer_customer}的产品为{payer_product}数据成功')
        except Exception as e:
            print(f'监控三开始处理{payer_sales_name}的付方签约名为{payer_customer}的产品为{payer_product}数据失败')

# if __name__ == "__main__":
#     a = Monitor3()
#     b = a.run()
#     print(b)
