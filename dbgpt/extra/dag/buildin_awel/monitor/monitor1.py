from dbgpt.extra.dag.buildin_awel.monitor import monitor1_data
from dbgpt.extra.dag.buildin_awel.monitor.api import get_past_working_days


class Monitor1():
    def __init__(self):
        self.alert_list = []
        try:
            print('监控一中开始获取工作日')
            self.d_1_trx_date = ','.join(get_past_working_days(1))
            self.d_1_d_7_trx_date = ','.join(get_past_working_days(7))
            self.d_1_d_15_trx_date = ','.join(get_past_working_days(15))
            self.d_1_d_30_trx_date = ','.join(get_past_working_days(30))
            self.d_1_d_45_trx_date = ','.join(get_past_working_days(45))


        except Exception as e:
            print('监控一中获得工作日失败')
            raise e

        try:
            print('监控一中开始行业线数据')
            self.d_1_industry_line_data = monitor1_data.get_industry_line_data_by_stat_in_monitor1(self.d_1_trx_date)[0]
            self.d_1_d_7_industry_line_data = \
            monitor1_data.get_industry_line_data_by_stat_in_monitor1(self.d_1_d_7_trx_date)[0]
            self.d_1_d_15_industry_line_data = \
            monitor1_data.get_industry_line_data_by_stat_in_monitor1(self.d_1_d_15_trx_date)[0]
            self.d_1_d_30_industry_line_data = \
            monitor1_data.get_industry_line_data_by_stat_in_monitor1(self.d_1_d_30_trx_date)[0]
            self.d_1_d_45_industry_line_data = \
            monitor1_data.get_industry_line_data_by_stat_in_monitor1(self.d_1_d_45_trx_date)[0]

        except Exception as e:
            print('监控一中开始行业线数据失败')
            raise e

    def run(self):
        sales_name_list = set()
        try:
            print('监控一开始获取所有销售')
            data = monitor1_data.get_data_by_stat_in_monitor1(self.d_1_d_45_trx_date)
            for item in data:
                sales_name_list.add(item['SALES_NAME'])
        except Exception as e:
            print('监控一开始获取所有销售失败')

        for sales_name in sales_name_list:
            self.deal_sales_name(sales_name)

        return self.alert_list

    def deal_sales_name(self, sales_name, ):
        customer_list = set()
        try:
            print(f'监控一开始获取{sales_name}的商户签约名')
            data = monitor1_data.get_data_by_stat_in_monitor1(trx_date=self.d_1_d_45_trx_date, sales_name=sales_name)

            for item in data:
                customer_list.add(item['STAT_DISPAYSIGNEDNAME'])
        except Exception as e:
            print(f'监控一开始获取{sales_name}的商户签约名失败！')
            return

        for customer in customer_list:
            self.deal_customer(sales_name, customer)

    def deal_customer(self, sales_name, customer):
        try:
            print(f'监控一开始获取{sales_name}的商户签约名为{customer}的数据')
            d_1_data = monitor1_data.get_data_by_stat_in_monitor1(trx_date=self.d_1_trx_date, sales_name=sales_name,
                                                                  stat_dispaysignedname=customer)[0]
            d_1_d_7_data = monitor1_data.get_data_by_stat_in_monitor1(trx_date=self.d_1_d_7_trx_date,
                                                                      sales_name=sales_name,
                                                                      stat_dispaysignedname=customer)[0]
            d_1_d_15_data = monitor1_data.get_data_by_stat_in_monitor1(trx_date=self.d_1_d_15_trx_date,
                                                                       sales_name=sales_name,
                                                                       stat_dispaysignedname=customer)[0]
            d_1_d_30_data = monitor1_data.get_data_by_stat_in_monitor1(trx_date=self.d_1_d_30_trx_date,
                                                                       sales_name=sales_name,
                                                                       stat_dispaysignedname=customer)[0]
            d_1_d_45_data = monitor1_data.get_data_by_stat_in_monitor1(trx_date=self.d_1_d_45_trx_date,
                                                                       sales_name=sales_name,
                                                                       stat_dispaysignedname=customer)[0]
        except Exception as e:
            print(f'监控一开始获取{sales_name}的商户签约名为{customer}的数据失败')
            return

        try:
            '''
                ([D-1]交易金额- 前7天日均交易金额）的绝对值>=100000
                （【商户交易笔数环比】-【行业交易笔数环比】）的绝对值>=20%
                【商户交易笔数环比】：[D-1]交易笔数/前X天日均交易笔数-1,groupzby 商户签约名
                【行业交易笔数环比】[D-1]交易笔数/前X天日均交易笔数-1，不需要group by 商户签约名
                X=7，15，30，45
            '''
            print(f'监控一开始处理{sales_name}的商户签约名为{customer}的数据')
            if abs(float(d_1_data['SUCCESS_AMOUNT']) - float(d_1_d_7_data['SUCCESS_AMOUNT']) / 7) >= 100000:

                # X=7
                customer_success_count = float(d_1_data['SUCCESS_COUNT'])/float(d_1_d_7_data['SUCCESS_COUNT'])-1
                industry_line_success_count = float(self.d_1_industry_line_data['SUCCESS_COUNT'])/float(self.d_1_d_7_industry_line_data['SUCCESS_COUNT'])-1
                if abs(customer_success_count-industry_line_success_count) < 0.2:
                    return
                # X=15
                customer_success_count = float(d_1_data['SUCCESS_COUNT']) / float(d_1_d_15_data['SUCCESS_COUNT']) - 1
                industry_line_success_count = float(self.d_1_industry_line_data['SUCCESS_COUNT']) / float(self.d_1_d_15_industry_line_data['SUCCESS_COUNT']) - 1
                if abs(customer_success_count - industry_line_success_count) < 0.2:
                    return
                # X=30
                customer_success_count = float(d_1_data['SUCCESS_COUNT']) / float(
                    d_1_d_30_data['SUCCESS_COUNT']) - 1
                industry_line_success_count = float(self.d_1_industry_line_data['SUCCESS_COUNT']) / float(
                    self.d_1_d_30_industry_line_data['SUCCESS_COUNT']) - 1
                if abs(customer_success_count - industry_line_success_count) < 0.2:
                    return
                # X=45
                customer_success_count = float(d_1_data['SUCCESS_COUNT']) / float(
                    d_1_d_45_data['SUCCESS_COUNT']) - 1
                industry_line_success_count = float(self.d_1_industry_line_data['SUCCESS_COUNT']) / float(
                    self.d_1_d_45_industry_line_data['SUCCESS_COUNT']) - 1
                if abs(customer_success_count - industry_line_success_count) < 0.2:
                    return

                print(f'监控一{sales_name}的商户签约名为{customer}的数据异常条件满足')

                reason = self.find_reason(sales_name, customer)

                self.alert_list.append({
                    'title': '交易笔数波动异常',
                    'name': sales_name,
                    'content': f'商户签约名:{customer}，昨日交易金额{float(d_1_data["SUCCESS_COUNT"])/10000:.2f}万元，环比{"上升" if customer_success_count>0 else "下降"}{customer_success_count*100:.2f}%（商户交易笔数环比）',
                    'reason': reason
                })

        except Exception as e:
                print(f'监控一开始处理{sales_name}的商户签约名为{customer}的数据失败')


    def find_reason(self, sales_name, customer):
        print(f'监控一开始处理{sales_name}的商户签约名为{customer}的数据异常归因')
        return []
        pass
