from dbgpt.extra.dag.buildin_awel.monitor import monitor2_data
from dbgpt.extra.dag.buildin_awel.monitor.api import get_past_working_days


class Monitor2:
    def __init__(self):
        self.alert_list = []
        try:
            print('监控二中开始获取工作日')
            self.d_1_date = ','.join(get_past_working_days(1))
        except Exception as e:
            raise e


    def run(self):
        self.run_by_stat()
        self.run_by_payer()
        return self.alert_list

    def run_by_payer(self):
        print('监控二(付方签约名维度)开始执行')
        payer_sales_name_list = set()
        try:
            print('监控二开始获取所有付方销售')
            data = monitor2_data.get_data_by_payer_in_monitor2(self.d_1_date )
            for item in data:
                payer_sales_name_list.add(item['PAYER_SALES_NAME'])
        except Exception as e:
            print('监控二开始获取所有付方销售失败')

        for payer_sales_name in payer_sales_name_list:
            if payer_sales_name is not None:
                self.deal_payer_sales_name(payer_sales_name)

    def deal_payer_sales_name(self, payer_sales_name):
        payer_customer_list = set()
        try:
            print(f'监控二开始获取{payer_sales_name}的付方签约名')
            data = monitor2_data.get_data_by_payer_in_monitor2(trx_date=self.d_1_date, payer_sales_name=payer_sales_name)
            for item in data:
                payer_customer_list.add(item['PAYER_CUSTOMER_SIGNEDNAME'])
        except Exception as e:
            print(f'监控二开始获取{payer_sales_name}的付方签约名失败！')
            return

        for payer_customer in payer_customer_list:
            self.deal_payer_customer(payer_sales_name, payer_customer)


    def deal_payer_customer(self, payer_sales_name, payer_customer):
        try:
            print(f'监控二开始获取{payer_sales_name}的付方签约名为{payer_customer}的数据')
            d_1_data = monitor2_data.get_data_by_payer_in_monitor2(trx_date=self.d_1_date, payer_sales_name=payer_sales_name,
                                                                    payer_customer_signedname=payer_customer)[0]

        except Exception as e:
            print(f'监控二开始获取{payer_sales_name}的付方签约名为{payer_customer}的数据失败')
            return

        try:
            '''
            退款率=退款笔数/交易笔数
            (退款率>30%)
            '''
            print(f'监控二开始处理{payer_sales_name}的付方签约名为{payer_customer}的数据')
            if float(d_1_data['SUCCESS_COUNT']) != 0 and float(d_1_data['REFUND_COUNT'])/float(d_1_data['SUCCESS_COUNT']) > 0.3:
                self.alert_list.append({
                    'name': payer_sales_name,
                    'title': '退款笔数波动异常',
                    'type': '付方签约名',
                    'customer_name': payer_customer,
                    'content': f'昨日退款波动超过30%，退款率{float(d_1_data["REFUND_COUNT"])/float(d_1_data["SUCCESS_COUNT"])*100:.2f}%,请关注',
                    #波动详情：    昨日退款波动超过30%，退款率<text_tag color=orange>0.61%</text_tag>，请关注
                    'content_rich': f"波动详情：    昨日退款波动超过30%，退款率<text_tag color= orange>{float(d_1_data['REFUND_COUNT'])/float(d_1_data['SUCCESS_COUNT'])*100:.2f}%</text_tag>，请关注。"

                })


        except Exception as e:
            print(f'监控二开始处理{payer_sales_name}的付方签约名为{payer_customer}的数据失败')

    def run_by_stat(self):
        print('监控二(商户签约名维度)开始执行')
        sales_name_list = set()
        try:
            print('监控二开始获取所有销售')
            data = monitor2_data.get_data_by_stat_in_monitor2(self.d_1_date)
            for item in data:
                sales_name_list.add(item['SALES_NAME'])
        except Exception as e:
            print('监控二开始获取所有销售失败')

        for sales_name in sales_name_list:
            self.deal_sales_name(sales_name)



    def deal_sales_name(self, sales_name):
        customer_list = set()
        try:
            print(f'监控二开始获取{sales_name}的商户签约名')
            data = monitor2_data.get_data_by_stat_in_monitor2(trx_date=self.d_1_date, sales_name=sales_name)
            for item in data:
                customer_list.add(item['STAT_DISPAYSIGNEDNAME'])
        except Exception as e:
            print(f'监控二开始获取{sales_name}的商户签约名失败！')
            return

        for customer in customer_list:
            self.deal_customer(sales_name, customer)

    def deal_customer(self, sales_name, customer):
        try:
            print(f'监控二开始获取{sales_name}的商户 签约名为{customer}的数据')
            d_1_data = monitor2_data.get_data_by_stat_in_monitor2(trx_date=self.d_1_date, sales_name=sales_name,
                                                                    stat_dispaysignedname=customer)[0]

        except Exception as e:
            print(f'监控二开始获取{sales_name}的商户签约名为{customer}的数据失败')
            return

        try:
            '''
            退款率=退款笔数/交易笔数
            (退款率>30%)
            '''
            print(f'监控二开始处理{sales_name}的商户签约名为{customer}的数据')
            if float(d_1_data['SUCCESS_COUNT']) != 0 and float(d_1_data['REFUND_COUNT'])/float(d_1_data['SUCCESS_COUNT']) > 0.3:
                self.alert_list.append({
                    'name': sales_name,
                    'title': '退款笔数波动异常',
                    'type': '商户签约名',
                    'customer_name': customer,
                    'content': f'昨日退款波动超过30%，退款率{float(d_1_data["REFUND_COUNT"])/float(d_1_data["SUCCESS_COUNT"])*100:.2f}%,请关注',
                    'content_rich': f"波动详情：    昨日退款波动超过30%，退款率<text_tag color= orange>{float(d_1_data['REFUND_COUNT'])/float(d_1_data['SUCCESS_COUNT'])*100:.2f}%</text_tag>，请关注。"

                })


        except Exception as e:
            print(f'监控二开始处理{sales_name}的商户签约名为{customer}的数据失败')



# if __name__ == "__main__":
#     a = Monitor2()
#     b = a.run()
#     print(b)