from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict

from dbgpt.extra.dag.buildin_awel.monitor.airline_monitor_handler import AirlineMonitorDataHandler


class Monitor4(AirlineMonitorDataHandler):
    def __init__(self):
        super().__init__()
        self.alert_list = []

    def prepare_data(self):
        self.alert_list = []
        try:
            print('监控四中开始获取日期')
            today = datetime.now()
            # 自然日
            self.d_1_d_7_date = ','.join([(today - timedelta(days=x + 1)).strftime("%Y-%m-%d") for x in range(7)])
            self.d_8_d_14_date = ','.join([(today - timedelta(days=x + 8)).strftime("%Y-%m-%d") for x in range(7)])
            self.original_scene_dict = self.get_original_scene_dict()

        except Exception as e:
            raise e

    def run(self):
        self.prepare_data()
        print('监控四(商户签约名维度)开始执行')
        sales_name_list = set()
        try:
            d_1_d_7_success_amount = 0
            d_8_d_14_success_amount = 0
            print('监控四开始获取所有销售')
            d_1_d_7_data = self.monitor4_data.get_data_by_stat_in_monitor4(self.d_1_d_7_date)
            d_8_d_14_data = self.monitor4_data.get_data_by_stat_in_monitor4(self.d_8_d_14_date)
            for item in d_1_d_7_data:
                sales_name_list.add(item['SALES_NAME'])
                d_1_d_7_success_amount += float(item['SUCCESS_AMOUNT'])
            for item in d_8_d_14_data:
                sales_name_list.add(item['SALES_NAME'])
                d_8_d_14_success_amount += float(item['SUCCESS_AMOUNT'])

            # 除数为0跳过
            if d_8_d_14_success_amount == 0:
                return

            self.market_fluctuation = d_1_d_7_success_amount / d_8_d_14_success_amount


        except Exception as e:
            print('监控四开始获取所有销售失败')

        d1d7_result_sales, d1d7_result_sales_custom, d1d7_result_sales_custom_produc = self.build_d_n_stat_datas_by_some(
            "d1d7"
        )
        d8d14_result_sales, d8d14_result_sales_custom, d8d14_result_sales_custom_produc = self.build_d_n_stat_datas_by_some(
            "d8d14"
        )

        for sales_name in sales_name_list:
            self.deal_sales_name(
                d1d7_result_sales,
                d1d7_result_sales_custom,
                d1d7_result_sales_custom_produc,
                d8d14_result_sales,
                d8d14_result_sales_custom,
                d8d14_result_sales_custom_produc,
                sales_name
            )
        def custom_sort(data):
            if data['data']['proportion_type'] == '下降':
                return (0, data['data']['sales_name'], data['data']['proportion_value'])
            return (1, data['data']['sales_name'], -data['data']['proportion_value'])

        self.alert_list = sorted(self.alert_list, key=custom_sort)

        return self.alert_list

    def build_d_n_stat_datas_by_some(self, days_type):
        """按1、销售，2、销售、签约名，3、销售、签约名、产品分组，构造数据"""

        d_n_datas = []
        if days_type == "d1d7":
            d_n_datas = self.monitor4_data.get_data_by_stat_in_monitor4(
                trx_date=self.d_1_d_7_date
            )
        if days_type == "d8d14":
            d_n_datas = self.monitor4_data.get_data_by_stat_in_monitor4(
                trx_date=self.d_8_d_14_date
            )
        print(f'监控四({days_type})构造条数: {len(d_n_datas)}！')
        for rec in d_n_datas:
            if rec["SALES_NAME"] is None:
                rec["SALES_NAME"] = "None"
            if rec["STAT_DISPAYSIGNEDNAME"] is None:
                rec["STAT_DISPAYSIGNEDNAME"] = "None"
            if rec["PAYER_DISPAYSIGNEDNAME"] is None:
                rec["PAYER_DISPAYSIGNEDNAME"] = "None"
        result_sales = defaultdict(list)
        result_sales_custom = defaultdict(list)
        result_sales_custom_produc = defaultdict(list)
        for rec in d_n_datas:
            k = str(rec["SALES_NAME"])
            result_sales[k].append(rec)
        for rec in d_n_datas:
            k = str(rec["SALES_NAME"]) + '#_#' + str(rec["STAT_DISPAYSIGNEDNAME"])
            result_sales_custom[k].append(rec)
        for rec in d_n_datas:
            k = str(rec["SALES_NAME"]) + '#_#' + str(rec["STAT_DISPAYSIGNEDNAME"]) + '#_#' + str(
                rec["PAYER_DISPAYSIGNEDNAME"])
            result_sales_custom_produc[k].append(rec)
        return result_sales, result_sales_custom, result_sales_custom_produc

    def deal_sales_name(
            self,
            d1d7_result_sales,
            d1d7_result_sales_custom,
            d1d7_result_sales_custom_produc,
            d8d14_result_sales,
            d8d14_result_sales_custom,
            d8d14_result_sales_custom_produc,
            sales_name
    ):
        customer_list = set()
        d_1_d_7_customer_to_success_amount = {}
        d_8_d_14_customer_to_success_amount = {}
        try:
            print(f'监控四开始获取{sales_name}的商户签约名')
            d_1_d_7_data = d1d7_result_sales[sales_name]
            d_8_d_14_data = d8d14_result_sales[sales_name]
            # d_1_d_7_data = self.monitor4_data.get_data_by_stat_in_monitor4(
            #     trx_date=self.d_1_d_7_date,
            #     sales_name=sales_name
            # )
            # d_8_d_14_data = self.monitor4_data.get_data_by_stat_in_monitor4(
            #     trx_date=self.d_8_d_14_date,
            #     sales_name=sales_name
            # )
            for item in d_1_d_7_data:
                customer_list.add(item['STAT_DISPAYSIGNEDNAME'])
                d_1_d_7_customer_to_success_amount[item['STAT_DISPAYSIGNEDNAME']] = float(item['SUCCESS_AMOUNT'])
            for item in d_8_d_14_data:
                customer_list.add(item['STAT_DISPAYSIGNEDNAME'])
                d_8_d_14_customer_to_success_amount[item['STAT_DISPAYSIGNEDNAME']] = float(item['SUCCESS_AMOUNT'])
        except Exception as e:
            print(f'监控四开始获取{sales_name}的商户签约名失败！')
            return

        for customer in customer_list:
            d_1_d_7_customer_success_amount = 0
            d_8_d_14_customer_success_amount = 0
            if customer in d_1_d_7_customer_to_success_amount:
                d_1_d_7_customer_success_amount = d_1_d_7_customer_to_success_amount[customer]
            if customer in d_8_d_14_customer_to_success_amount:
                d_8_d_14_customer_success_amount = d_8_d_14_customer_to_success_amount[customer]
            # 除数为0，抛弃
            if d_8_d_14_customer_to_success_amount == 0:
                continue
            self.deal_customer(
                d1d7_result_sales_custom,
                d1d7_result_sales_custom_produc,
                d8d14_result_sales_custom,
                d8d14_result_sales_custom_produc,
                sales_name,
                customer,
                d_1_d_7_customer_success_amount,
                d_8_d_14_customer_success_amount)

    def deal_customer(
            self,
            d1d7_result_sales_custom,
            d1d7_result_sales_custom_produc,
            d8d14_result_sales_custom,
            d8d14_result_sales_custom_produc,
            sales_name,
            customer,
            d_1_d_7_customer_success_amount: float,
            d_8_d_14_customer_success_amount: float
    ):
        payer_list = set()
        try:
            print(f'监控四开始获取{sales_name}的商户签约名为{customer}的数据')
            d_1_d_7_data = d1d7_result_sales_custom[sales_name + "#_#" + customer]
            d_8_d_14_data = d8d14_result_sales_custom[sales_name + "#_#" + customer]
            # d_1_d_7_data = self.monitor4_data.get_data_by_stat_in_monitor4(
            #     trx_date=self.d_1_d_7_date,
            #     sales_name=sales_name,
            #     stat_dispaysignedname=customer
            # )
            # d_8_d_14_data = self.monitor4_data.get_data_by_stat_in_monitor4(
            #     trx_date=self.d_8_d_14_date,
            #     sales_name=sales_name,
            #     stat_dispaysignedname=customer
            # )

            for item in d_1_d_7_data:
                payer_list.add(item['PAYER_DISPAYSIGNEDNAME'])
            for item in d_8_d_14_data:
                payer_list.add(item['PAYER_DISPAYSIGNEDNAME'])

        except Exception as e:
            print(f'监控四开始获取{sales_name}的商户签约名为{customer}的数据失败')
            return

        for payer in payer_list:
            self.deal_payer(
                d1d7_result_sales_custom_produc,
                d8d14_result_sales_custom_produc,
                sales_name,
                customer,
                d_1_d_7_customer_success_amount,
                d_8_d_14_customer_success_amount,
                payer
            )

    def deal_payer(
            self,
            d1d7_result_sales_custom_produc,
            d8d14_result_sales_custom_produc,
            sales_name,
            customer,
            d_1_d_7_customer_success_amount,
            d_8_d_14_customer_success_amount,
            payer
    ):
        try:
            print(f'监控四开始获取{sales_name}的商户签约名为{customer}的付方签约名为{payer}的数据')
            d_1_d_7_data = d1d7_result_sales_custom_produc[sales_name + "#_#" + customer + "#_#" + payer]
            d_8_d_14_data = d8d14_result_sales_custom_produc[sales_name + "#_#" + customer + "#_#" + payer]
            # d_1_d_7_data = self.monitor4_data.get_data_by_stat_in_monitor4(
            #     trx_date=self.d_1_d_7_date,
            #     sales_name=sales_name,
            #     stat_dispaysignedname=customer,
            #     payer=payer
            # )
            # d_8_d_14_data = self.monitor4_data.get_data_by_stat_in_monitor4(
            #     trx_date=self.d_8_d_14_date,
            #     sales_name=sales_name,
            #     stat_dispaysignedname=customer,
            #     payer=payer
            # )

            print(f'监控四开始处理{sales_name}的商户签约名为{customer}的付方签约名为{payer}的数据')

            d_1_d_7_payer_success_amount = 0
            d_8_d_14_payer_success_amount = 0
            for item in d_1_d_7_data:
                d_1_d_7_payer_success_amount += float(item['SUCCESS_AMOUNT'])
            for item in d_8_d_14_data:
                d_8_d_14_payer_success_amount += float(item['SUCCESS_AMOUNT'])

            '''
            交易金额周环比差值，付方交易金额本周比上周，与收方交易金额本周比上周差值
            波动异常参数：
            [图片]
            A：收方商编=10012407595
            付方SUM（D-1～D-7）/SUM（D-8～D-14）与航司SUM（D-1～D-7）/SUM（D-8～D-14）
            B：收方商编=10034228238
            付方SUM（D-1～D-7）/SUM（D-8～D-14）与航司SUM（D-1～D-7）/SUM（D-8～D-14）
            '''
            # 除数为0，抛弃
            if d_8_d_14_payer_success_amount == 0:
                return
            difference = d_1_d_7_payer_success_amount / d_8_d_14_payer_success_amount - d_1_d_7_customer_success_amount / d_8_d_14_customer_success_amount

            flag = False

            if d_1_d_7_payer_success_amount >= 1500 * 10 ** 4:
                if difference > 0.2 or difference < -0.15:
                    flag = True
            elif d_8_d_14_payer_success_amount >= 100 * 10 ** 4:
                if difference > 0.5 or difference < -0.5:
                    flag = True
            elif d_1_d_7_payer_success_amount >= 50 * 10 ** 4:
                if difference > 0.8 or difference < -0.8:
                    flag = True

            if flag is False:
                return
            print(f'监控四开始处理{sales_name}的商户签约名为{customer}的付方签约名为{payer}的数据归因')

            '''
            归因输出中还有细化，商编和场景字段维度
            
            付方名称，航司——商编+场景字段，近7天充值金额，环比上周上升/下降**，高于/低于大盘**
            '''

            for item2 in d_8_d_14_data:
                for item1 in d_1_d_7_data:
                    if item1['CUSTOMER_NO'] == item2['CUSTOMER_NO']:
                        if float(item2["SUCCESS_AMOUNT"]) == 0 or d_8_d_14_customer_success_amount == 0:
                            continue
                        difference = float(item1["SUCCESS_AMOUNT"]) / float(item2[
                                                                                "SUCCESS_AMOUNT"]) - d_1_d_7_customer_success_amount / d_8_d_14_customer_success_amount
                        orig_scene = self.get_original_scene_by_merchant_no(
                            self.original_scene_dict,
                            item1["CUSTOMER_NO"]
                        )
                        fluctuation = float(item1["SUCCESS_AMOUNT"]) / float(
                            item2["SUCCESS_AMOUNT"]) - self.market_fluctuation
                        content = f'付方名称:{payer}，航司:{customer}——商编:{item1["CUSTOMER_NO"]}+场景字段:{orig_scene}，近7天充值金额，环比上周{"上升" if difference > 0 else "下降"}{abs(difference * 100):.2f}%，{"高于" if fluctuation > 0 else "低于"}大盘{abs(fluctuation * 100):.2f}%'
                        subcontent = f"近7天充值金额，环比上周{'上升' if difference > 0 else '下降'}**<font color={'green' if difference > 0 else 'red'}>{abs(difference * 100):.2f}%</font>**，{'高于' if fluctuation > 0 else '低于'}大盘**<font color={'green' if fluctuation > 0 else 'red'}>{abs(fluctuation * 100):.2f}%</font>**"

                        self.alert_list.append({
                            'name': sales_name,
                            'title': '深航/国航充值业务',
                            'content': content,
                            'payer_customer_signedname': f'<font color=green>{payer}</font>',
                            'payer_customer_signedname_text': payer,
                            'stat_dispaysignedname': customer,
                            'customer_no': item1["CUSTOMER_NO"],
                            'payer_business_scene': orig_scene,
                            'sub_content_rich': subcontent,
                            'data': {
                                'monitor_type': '4',
                                'sales_name': sales_name,
                                'customer_name': customer,
                                'customer_no': item1['CUSTOMER_NO'],
                                'payer_customer_name': payer,
                                'orig_scene': orig_scene,
                                'd_1_d_7_payer_success_amount': d_1_d_7_payer_success_amount,
                                'proportion_type': '上升' if difference > 0 else '下降',
                                'proportion_value': difference,
                                'fluctuation_type': '高于' if fluctuation > 0 else '低于',
                                'fluctuation_value': fluctuation,
                                'remarks': '付方签约名是payer_customer_name，航司是customer_name，场景是orig_scene,近7天充值金额是d_1_d_7_payer_success_amount，环比值是proportion_value，相比于大盘是fluctuation_value'
                            }
                        })

        except Exception as e:
            print(f'监控四开始获取{sales_name}的商户签约名为{customer}的付方签约名为{payer}的数据失败')
            return
# if __name__ == "__main__":
#     a = Monitor4()
#     b = a.run()
#     print(b)