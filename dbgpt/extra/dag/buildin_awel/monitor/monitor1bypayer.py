from dbgpt.extra.dag.buildin_awel.monitor import monitor1bypayer_data
from dbgpt.extra.dag.buildin_awel.monitor.api import get_past_working_days


class Monitor1ByPayer:
    def __init__(self):
        self.alert_list = []
        try:
            print('监控一中开始获取工作日')
            self.d_1_trx_date = ','.join(get_past_working_days(1))
            self.d_2_trx_date = ','.join(get_past_working_days(2)).split(',')[1]
            self.d_1_d_7_trx_date = ','.join(get_past_working_days(7))
            self.d_1_d_15_trx_date = ','.join(get_past_working_days(15))
            self.d_1_d_30_trx_date = ','.join(get_past_working_days(30))
            self.d_1_d_45_trx_date = ','.join(get_past_working_days(45))


        except Exception as e:
            print('监控一中获得工作日失败')
            raise e

        try:
            print('监控一中开始行业线数据')
            self.d_1_industry_line_data = monitor1bypayer_data.get_industry_line_data_by_payer_in_monitor1(self.d_1_trx_date)[0]
            self.d_1_d_7_industry_line_data = \
                monitor1bypayer_data.get_industry_line_data_by_payer_in_monitor1(self.d_1_d_7_trx_date)[0]
            self.d_1_d_15_industry_line_data = \
                monitor1bypayer_data.get_industry_line_data_by_payer_in_monitor1(self.d_1_d_15_trx_date)[0]
            self.d_1_d_30_industry_line_data = \
                monitor1bypayer_data.get_industry_line_data_by_payer_in_monitor1(self.d_1_d_30_trx_date)[0]
            self.d_1_d_45_industry_line_data = \
                monitor1bypayer_data.get_industry_line_data_by_payer_in_monitor1(self.d_1_d_45_trx_date)[0]

        except Exception as e:
            print('监控一中开始行业线数据失败')
            raise e

    def run(self):
        print('监控一(付方签约名维度)开始执行')
        payer_sales_name_list = set()
        try:
            print('监控一开始获取所有付方销售')
            data = monitor1bypayer_data.get_data_by_payer_in_monitor1(self.d_1_d_45_trx_date)
            for item in data:
                payer_sales_name_list.add(item['PAYER_SALES_NAME'])
        except Exception as e:
            print('监控一开始获取所有付方销售失败')

        for payer_sales_name in payer_sales_name_list:
            if payer_sales_name is None:
                continue
            self.deal_sales_name(payer_sales_name)

        return self.alert_list
        pass

    def deal_sales_name(self, payer_sales_name, ):
        customer_list = set()
        try:
            print(f'监控一开始获取付方销售({payer_sales_name})的付方签约名')
            data = monitor1bypayer_data.get_data_by_payer_in_monitor1(trx_date=self.d_1_d_45_trx_date, payer_sales_name=payer_sales_name)

            for item in data:
                customer_list.add(item['PAYER_CUSTOMER_SIGNEDNAME'])
        except Exception as e:
            print(f'监控一开始获取付方销售({payer_sales_name})的付方签约名失败！')
            return

        for customer in customer_list:
            self.deal_customer(payer_sales_name, customer)

    def deal_customer(self, payer_sales_name, customer):
        try:
            print(f'监控一开始获取{payer_sales_name}的付方签约名为{customer}的数据')
            d_1_data = monitor1bypayer_data.get_data_by_payer_in_monitor1(trx_date=self.d_1_trx_date, payer_sales_name=payer_sales_name,
                                                                  payer_customer_signedname=customer)[0]
            d_1_d_7_data = monitor1bypayer_data.get_data_by_payer_in_monitor1(trx_date=self.d_1_d_7_trx_date,
                                                                      payer_sales_name=payer_sales_name,
                                                                      payer_customer_signedname=customer)[0]
            d_1_d_15_data = monitor1bypayer_data.get_data_by_payer_in_monitor1(trx_date=self.d_1_d_15_trx_date,
                                                                       payer_sales_name=payer_sales_name,
                                                                       payer_customer_signedname=customer)[0]
            d_1_d_30_data = monitor1bypayer_data.get_data_by_payer_in_monitor1(trx_date=self.d_1_d_30_trx_date,
                                                                       payer_sales_name=payer_sales_name,
                                                                       payer_customer_signedname=customer)[0]
            d_1_d_45_data = monitor1bypayer_data.get_data_by_payer_in_monitor1(trx_date=self.d_1_d_45_trx_date,
                                                                       payer_sales_name=payer_sales_name,
                                                                       payer_customer_signedname=customer)[0]
        except Exception as e:
            print(f'监控一开始获取{payer_sales_name}的付方签约名为{customer}的数据失败')
            return

        try:
            '''
                ([D-1]交易金额- 前7天日均交易金额）的绝对值>=100000
                （【付方交易笔数环比】-【行业交易笔数环比】）的绝对值>=20%
                【付方交易笔数环比】：[D-1]交易笔数/前X天日均交易笔数-1,group by 付款方签约名
                【行业交易笔数环比】[D-1]交易笔数/前X天日均交易笔数-1，不需要group by 商户签约名
                X=7，15，30，45
            '''
            print(f'监控一开始处理{payer_sales_name}的付方签约名为{customer}的数据')
            if abs(float(d_1_data['SUCCESS_AMOUNT']) - float(d_1_d_7_data['SUCCESS_AMOUNT']) / 7) >= 100000:

                # X=7
                customer_success_count = float(d_1_data['SUCCESS_COUNT']) / (
                        float(d_1_d_7_data['SUCCESS_COUNT']) / 7) - 1
                industry_line_success_count = float(self.d_1_industry_line_data['SUCCESS_COUNT']) / (
                        float(self.d_1_d_7_industry_line_data['SUCCESS_COUNT']) / 7) - 1
                if abs(customer_success_count - industry_line_success_count) < 0.2:
                    return
                # X=15
                customer_success_count = float(d_1_data['SUCCESS_COUNT']) / (
                        float(d_1_d_15_data['SUCCESS_COUNT']) / 15) - 1
                industry_line_success_count = float(self.d_1_industry_line_data['SUCCESS_COUNT']) / (
                        float(self.d_1_d_15_industry_line_data['SUCCESS_COUNT']) / 15) - 1
                if abs(customer_success_count - industry_line_success_count) < 0.2:
                    return
                # X=30
                customer_success_count = float(d_1_data['SUCCESS_COUNT']) / (float(
                    d_1_d_30_data['SUCCESS_COUNT']) / 30) - 1
                industry_line_success_count = float(self.d_1_industry_line_data['SUCCESS_COUNT']) / (float(
                    self.d_1_d_30_industry_line_data['SUCCESS_COUNT']) / 30) - 1
                if abs(customer_success_count - industry_line_success_count) < 0.2:
                    return
                # X=45
                customer_success_count = float(d_1_data['SUCCESS_COUNT']) / (float(
                    d_1_d_45_data['SUCCESS_COUNT']) / 45) - 1
                industry_line_success_count = float(self.d_1_industry_line_data['SUCCESS_COUNT']) / (float(
                    self.d_1_d_45_industry_line_data['SUCCESS_COUNT']) / 45) - 1
                if abs(customer_success_count - industry_line_success_count) < 0.2:
                    return

                print(f'监控一{payer_sales_name}的付方签约名为{customer}的数据异常条件满足')

                reason4 = self.find_reason4(payer_sales_name, customer)
                reason5 = self.find_reason5(payer_sales_name, customer)

                self.alert_list.append({
                    'title': '交易笔数波动异常',
                    'name': payer_sales_name,
                    'content': f'付方签约名:{customer}，昨日交易金额{float(d_1_data["SUCCESS_COUNT"]) / 10000:.2f}万元，环比{"上升" if customer_success_count > 0 else "下降"}{customer_success_count * 100:.2f}%（商户交易笔数环比）',
                    'reason4': '\n'.join(reason4),
                    'reason5': '\n'.join(reason5)
                })

        except Exception as e:
            print(f'监控一开始处理{payer_sales_name}的付方签约名为{customer}的数据失败!')


    def find_reason4(self, payer_sales_name, customer) -> list:
        print(f'监控一处理{payer_sales_name}的付方签约名为{customer}的数据异常归因4')
        reason4 = []
        '''
        1、产品交易波动异常
        归因④【付款方签约名+产品】
        ([D-1]交易金额- [D-2]交易金额）的绝对值>=100000
        - 交易环比（[D-1]交易金额/[D-2]交易金额-1
          - >100%——上升
          - <-50%——下降
        '''
        # 归因4
        try:
            d_1_data = monitor1bypayer_data.get_reason_4_data_by_payer_in_monitor1(trx_date=self.d_1_trx_date,
                                                                           payer_sales_name=payer_sales_name,
                                                                           payer_customer_signedname=customer)
            d_2_data = monitor1bypayer_data.get_reason_4_data_by_payer_in_monitor1(trx_date=self.d_2_trx_date,
                                                                           payer_sales_name=payer_sales_name,
                                                                           payer_customer_signedname=customer)
            d_1_d_45_data = monitor1bypayer_data.get_reason_4_data_by_payer_in_monitor1(trx_date=self.d_1_d_45_trx_date,
                                                                           payer_sales_name=payer_sales_name,
                                                                           payer_customer_signedname=customer)

            for d_2_item in d_2_data:
                d_2_success_amount = float(d_2_item['SUCCESS_AMOUNT'])
                d_1_success_amount = 0
                d_1_success_count = 0
                for d_1_item in d_1_data:
                    if d_1_item['PRODUCT'] == d_2_item['PRODUCT']:
                        d_1_success_amount = float(d_1_item['SUCCESS_AMOUNT'])
                        d_1_success_count = float(d_1_item['SUCCESS_COUNT'])
                        break
                if abs(d_1_success_amount - d_2_success_amount) >= 100000:
                    if d_1_success_amount / d_2_success_amount - 1 > 1:
                        reason4.append(
                            f'付方签约名:{customer},产品:{d_2_item["PRODUCT"]},昨日交易金额{d_1_success_amount/10000:.2f}万元，环比上升{abs(d_1_success_amount / d_2_success_amount - 1) * 100:.2f}%')
                    if d_1_success_amount / d_2_success_amount - 1 < -0.5:
                        reason4.append(
                            f'付方签约名:{customer},产品:{d_2_item["PRODUCT"]},昨日交易金额{d_1_success_amount/10000:.2f}万元，环比下降{abs(d_1_success_amount / d_2_success_amount - 1) * 100:.2f}%')

        except Exception as e:
            print('归因4处理错误')

        return reason4


    def find_reason5(self, payer_sales_name, customer) -> list:
        '''
            归因⑤【付款方签约名+商户签约名】
            ([D-1]交易金额- [D-2]交易金额）的绝对值>=100000
            - 交易环比（[D-1]交易金额/[D-2]交易金额-1
              - >100%——上升
              - <-50%——下降
        '''
        print(f'监控一处理{payer_sales_name}的付方签约名为{customer}的数据异常归因5')
        reason5 = []
        # 归因5
        try:
            d_1_data = monitor1bypayer_data.get_reason_5_data_by_payer_in_monitor1(trx_date=self.d_1_trx_date,
                                                                                   payer_sales_name=payer_sales_name,
                                                                                   payer_customer_signedname=customer)
            d_2_data = monitor1bypayer_data.get_reason_5_data_by_payer_in_monitor1(trx_date=self.d_2_trx_date,
                                                                                   payer_sales_name=payer_sales_name,
                                                                                   payer_customer_signedname=customer)
            d_1_d_45_data = monitor1bypayer_data.get_reason_5_data_by_payer_in_monitor1(trx_date=self.d_1_d_45_trx_date,
                                                                                        payer_sales_name=payer_sales_name,
                                                                                        payer_customer_signedname=customer)

            for d_2_item in d_2_data:
                d_2_success_amount = float(d_2_item['SUCCESS_AMOUNT'])
                d_1_success_amount = 0
                d_1_success_count = 0
                for d_1_item in d_1_data:
                    if d_1_item['STAT_DISPAYSIGNEDNAME'] == d_2_item['STAT_DISPAYSIGNEDNAME']:
                        d_1_success_amount = float(d_1_item['SUCCESS_AMOUNT'])
                        d_1_success_count = float(d_1_item['SUCCESS_COUNT'])
                        break
                if abs(d_1_success_amount - d_2_success_amount) >= 100000:
                    if d_1_success_amount / d_2_success_amount - 1 > 1:
                        reason5.append(
                            f'主要影响的收方商户签约名:{d_2_item["STAT_DISPAYSIGNEDNAME"]},昨日交易金额{d_1_success_amount / 10000:.2f}万元，环比上升{abs(d_1_success_amount / d_2_success_amount - 1) * 100:.2f}%')
                    if d_1_success_amount / d_2_success_amount - 1 < -0.5:
                        reason5.append(
                            f'主要影响的收方商户签约名:{d_2_item["STAT_DISPAYSIGNEDNAME"]},昨日交易金额{d_1_success_amount / 10000:.2f}万元，环比上升{abs(d_1_success_amount / d_2_success_amount - 1) * 100:.2f}%')



        except Exception as e:
            print('归因5处理错误')


        return reason5

if __name__ == "__main__":
    a = Monitor1ByPayer()
    b = a.run()
    print(b)