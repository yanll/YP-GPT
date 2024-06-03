from dbgpt.extra.dag.buildin_awel.monitor.airline_monitor_handler import AirlineMonitorDataHandler


class Monitor1ByStat(AirlineMonitorDataHandler):
    def __init__(self):
        super().__init__()
        self.alert_list = []

    def prepare_data(self):
        self.alert_list = []
        try:
            print('监控一中开始获取工作日')
            self.d_1_trx_date = ','.join(self.get_past_working_days(1))
            self.d_2_trx_date = ','.join(self.get_past_working_days(2)).split(',')[1]
            self.d_1_d_7_trx_date = ','.join(self.get_past_working_days(7))
            self.d_1_d_15_trx_date = ','.join(self.get_past_working_days(15))
            self.d_1_d_30_trx_date = ','.join(self.get_past_working_days(30))
            self.d_1_d_45_trx_date = ','.join(self.get_past_working_days(45))
            self.original_scene_dict = self.get_original_scene_dict()


        except Exception as e:
            print('监控一中获得工作日失败')
            raise e

        try:
            print('监控一中开始行业线数据')
            self.d_1_industry_line_data = \
                self.monitor1bystat_data.get_industry_line_data_by_stat_in_monitor1(self.d_1_trx_date)[0]
            self.d_1_d_7_industry_line_data = \
                self.monitor1bystat_data.get_industry_line_data_by_stat_in_monitor1(self.d_1_d_7_trx_date)[0]
            self.d_1_d_15_industry_line_data = \
                self.monitor1bystat_data.get_industry_line_data_by_stat_in_monitor1(self.d_1_d_15_trx_date)[0]
            self.d_1_d_30_industry_line_data = \
                self.monitor1bystat_data.get_industry_line_data_by_stat_in_monitor1(self.d_1_d_30_trx_date)[0]
            self.d_1_d_45_industry_line_data = \
                self.monitor1bystat_data.get_industry_line_data_by_stat_in_monitor1(self.d_1_d_45_trx_date)[0]

        except Exception as e:
            print('监控一中开始行业线数据失败')
            raise e

    def run(self):
        self.prepare_data()
        print('监控一(商户签约名维度)开始执行')
        sales_name_list = set()
        try:
            print('监控一开始获取所有销售')
            data = self.monitor1bystat_data.get_data_by_stat_in_monitor1(self.d_1_d_45_trx_date)
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
            data = self.monitor1bystat_data.get_data_by_stat_in_monitor1(trx_date=self.d_1_d_45_trx_date,
                                                                         sales_name=sales_name)

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
            d_1_data = \
                self.monitor1bystat_data.get_data_by_stat_in_monitor1(trx_date=self.d_1_trx_date, sales_name=sales_name,
                                                                      stat_dispaysignedname=customer)[0]
            d_1_d_7_data = self.monitor1bystat_data.get_data_by_stat_in_monitor1(trx_date=self.d_1_d_7_trx_date,
                                                                                 sales_name=sales_name,
                                                                                 stat_dispaysignedname=customer)[0]
            d_1_d_15_data = self.monitor1bystat_data.get_data_by_stat_in_monitor1(trx_date=self.d_1_d_15_trx_date,
                                                                                  sales_name=sales_name,
                                                                                  stat_dispaysignedname=customer)[0]
            d_1_d_30_data = self.monitor1bystat_data.get_data_by_stat_in_monitor1(trx_date=self.d_1_d_30_trx_date,
                                                                                  sales_name=sales_name,
                                                                                  stat_dispaysignedname=customer)[0]
            d_1_d_45_data = self.monitor1bystat_data.get_data_by_stat_in_monitor1(trx_date=self.d_1_d_45_trx_date,
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
                
                长期下滑：
                X=15，30，45时，商户交易笔数环比都是负数，且3个时期值均满足条件时抛出
                
                短期波动：
                X=7时，商户交易笔数环比都是负数
            '''
            print(f'监控一开始处理{sales_name}的商户签约名为{customer}的数据')

            def judge_long_term():
                # 长期下滑判断
                if abs(float(d_1_data['SUCCESS_AMOUNT']) - float(d_1_d_7_data['SUCCESS_AMOUNT']) / 7) >= 100000:

                    # X=15
                    customer_success_count = float(d_1_data['SUCCESS_COUNT']) / (
                            float(d_1_d_15_data['SUCCESS_COUNT']) / 15) - 1
                    industry_line_success_count = float(self.d_1_industry_line_data['SUCCESS_COUNT']) / (
                            float(self.d_1_d_15_industry_line_data['SUCCESS_COUNT']) / 15) - 1
                    if abs(customer_success_count - industry_line_success_count) < 0.2:
                        return
                    if customer_success_count >= 0:
                        return
                    # X=30
                    customer_success_count = float(d_1_data['SUCCESS_COUNT']) / (float(
                        d_1_d_30_data['SUCCESS_COUNT']) / 30) - 1
                    industry_line_success_count = float(self.d_1_industry_line_data['SUCCESS_COUNT']) / (float(
                        self.d_1_d_30_industry_line_data['SUCCESS_COUNT']) / 30) - 1
                    if abs(customer_success_count - industry_line_success_count) < 0.2:
                        return
                    if customer_success_count >= 0:
                        return
                    # X=45
                    customer_success_count = float(d_1_data['SUCCESS_COUNT']) / (float(
                        d_1_d_45_data['SUCCESS_COUNT']) / 45) - 1
                    industry_line_success_count = float(self.d_1_industry_line_data['SUCCESS_COUNT']) / (float(
                        self.d_1_d_45_industry_line_data['SUCCESS_COUNT']) / 45) - 1
                    if abs(customer_success_count - industry_line_success_count) < 0.2:
                        return
                    if customer_success_count >= 0:
                        return

                    print(f'监控一{sales_name}的商户签约名为{customer}的数据异常条件满足')

                    reason1, reason1_text = self.find_reason1(sales_name, customer)
                    reason2, reason2_text = self.find_reason2(sales_name, customer)
                    reason3, reason3_text = self.find_reason3(sales_name, customer)

                    self.alert_list.append({
                        'title': '交易笔数波动异常',
                        'name': sales_name,
                        'content': f'【长期下滑】商户签约名:{customer}，昨日交易金额{float(d_1_data["SUCCESS_AMOUNT"]) / 10000:.2f}万元，环比{"上升" if customer_success_count > 0 else "下降"}<text_tag color={"green" if customer_success_count > 0 else "red"} >{customer_success_count * 100:.2f}%</text_tag>（商户交易笔数环比）',
                        'content_text': f'【长期下滑】商户签约名:{customer}，昨日交易金额{float(d_1_data["SUCCESS_AMOUNT"]) / 10000:.2f}万元，环比{"上升" if customer_success_count > 0 else "下降"}{customer_success_count * 100:.2f}%（商户交易笔数环比）',
                        'reason1': '\n'.join(reason1),
                        'reason1_text': '\n'.join(reason1_text),
                        'reason2': '\n'.join(reason2),
                        'reason2_text': '\n'.join(reason2_text),
                        'reason3': '\n'.join(reason3),
                        'reason3_text': '\n'.join(reason3_text),
                    })

            def judge_short_term():
                if abs(float(d_1_data['SUCCESS_AMOUNT']) - float(d_1_d_7_data['SUCCESS_AMOUNT']) / 7) >= 100000:
                    # X=7
                    customer_success_count = float(d_1_data['SUCCESS_COUNT']) / (
                            float(d_1_d_7_data['SUCCESS_COUNT']) / 7) - 1
                    industry_line_success_count = float(self.d_1_industry_line_data['SUCCESS_COUNT']) / (
                            float(self.d_1_d_7_industry_line_data['SUCCESS_COUNT']) / 7) - 1
                    if abs(customer_success_count - industry_line_success_count) < 0.2:
                        return
                    if customer_success_count >= 0:
                        return
                    reason1, reason1_text = self.find_reason1(sales_name, customer)
                    reason2, reason2_text = self.find_reason2(sales_name, customer)
                    reason3, reason3_text = self.find_reason3(sales_name, customer)

                    self.alert_list.append({
                        'title': '交易笔数波动异常',
                        'name': sales_name,
                        'content': f'【短期波动】商户签约名:{customer}，昨日交易金额{float(d_1_data["SUCCESS_AMOUNT"]) / 10000:.2f}万元，环比{"上升" if customer_success_count > 0 else "下降"}<text_tag color={"green" if customer_success_count > 0 else "red"} >{customer_success_count * 100:.2f}%</text_tag>（商户交易笔数环比）',
                        'content_text': f'【短期波动】商户签约名:{customer}，昨日交易金额{float(d_1_data["SUCCESS_AMOUNT"]) / 10000:.2f}万元，环比{"上升" if customer_success_count > 0 else "下降"}{customer_success_count * 100:.2f}%（商户交易笔数环比）',
                        'reason1': '\n'.join(reason1),
                        'reason1_text': '\n'.join(reason1_text),
                        'reason2': '\n'.join(reason2),
                        'reason2_text': '\n'.join(reason2_text),
                        'reason3': '\n'.join(reason3),
                        'reason3_text': '\n'.join(reason3_text),
                    })

            judge_short_term()
            judge_long_term()

        except Exception as e:
            print(f'监控一开始处理{sales_name}的商户签约名为{customer}的数据失败')

    def find_reason1(self, sales_name, customer) -> list:
        print(f'监控一处理{sales_name}的商户签约名为{customer}的数据异常归因1')
        reason1 = []
        reason1_text = []
        '''
        1、产品&原始场景交易波动异常
        归因①【商户签约名+商户编号+原始场景】：
        - ([D-1]交易金额- [D-2]交易金额）的绝对值>=100000
        - [D-1]交易笔数/前X天日均交易笔数-1，上升或下降，取TOP3
        归因②【商户签约名+商户编号+原始场景+产品】：
        - ([D-1]交易金额- [D-2]交易金额）的绝对值>=10000
        - 交易环比（[D-1]交易金额/[D-2]交易金额-1
          - >150%——上升
          - <50%——下降
        '''
        # 归因1
        try:
            d_1_data = self.monitor1bystat_data.get_reason_1_data_by_stat_in_monitor1(trx_date=self.d_1_trx_date,
                                                                                      sales_name=sales_name,
                                                                                      stat_dispaysignedname=customer)
            d_2_data = self.monitor1bystat_data.get_reason_1_data_by_stat_in_monitor1(trx_date=self.d_2_trx_date,
                                                                                      sales_name=sales_name,
                                                                                      stat_dispaysignedname=customer)
            d_1_d_45_data = self.monitor1bystat_data.get_reason_1_data_by_stat_in_monitor1(
                trx_date=self.d_1_d_45_trx_date,
                sales_name=sales_name,
                stat_dispaysignedname=customer)

            reason_tmp = []
            reason_tmp_text = []
            for d_2_item in d_2_data:
                d_2_success_amount = float(d_2_item['SUCCESS_AMOUNT'])
                d_1_success_amount = 0
                d_1_success_count = 0
                for d_1_item in d_1_data:
                    if d_1_item['STAT_CUSTOMER_NO'] == d_2_item['STAT_CUSTOMER_NO']:
                        d_1_success_amount = float(d_1_item['SUCCESS_AMOUNT'])
                        d_1_success_count = float(d_1_item['SUCCESS_COUNT'])
                        break
                if abs(d_1_success_amount - d_2_success_amount) >= 100000:
                    d_1_d_45_success_count = 0
                    for d_1_d_45_item in d_1_d_45_data:

                        if d_1_d_45_item['STAT_CUSTOMER_NO'] == d_2_item['STAT_CUSTOMER_NO']:
                            d_1_d_45_success_count = float(d_1_d_45_item['SUCCESS_COUNT'])
                            break
                    if d_1_d_45_success_count == 0:
                        continue
                    difference = d_1_success_count / d_1_d_45_success_count - 1
                    orig_scene = self.get_original_scene_by_merchant_no(
                        self.original_scene_dict,
                        d_2_item["STAT_CUSTOMER_NO"]
                    )
                    reason_tmp.append((
                        difference,
                        f'归因一:商户签约名:{customer},商户编号:{d_2_item["STAT_CUSTOMER_NO"]},原始场景:{orig_scene}昨日交易金额{d_1_success_amount / 10000:.2f}万元，环比{"上升" if difference > 0 else "下降"}<text_tag color={"green" if difference > 0 else "red"} >{difference * 100:.2f}%</text_tag>'))
                    reason_tmp_text.append((
                        difference,
                        f'归因一:商户签约名:{customer},商户编号:{d_2_item["STAT_CUSTOMER_NO"]},原始场景:{orig_scene}昨日交易金额{d_1_success_amount / 10000:.2f}万元，环比{"上升" if difference > 0 else "下降"}{difference * 100:.2f}%'))
            if len(reason_tmp) > 3:
                reason_tmp.sort(key=lambda x: abs(x[0]), reverse=True)
                reason_tmp = reason_tmp[:3]
            if len(reason_tmp_text) > 3:
                reason_tmp_text.sort(key=lambda x: abs(x[0]), reverse=True)
                reason_tmp_text = reason_tmp_text[:3]

            for item in reason_tmp:
                reason1.append(item[1])
            for item in reason_tmp_text:
                reason1_text.append(item[1])

        except Exception as e:
            print('归因1处理错误')

        return reason1, reason1_text

    def find_reason2(self, sales_name, customer) -> list:
        print(f'监控一处理{sales_name}的商户签约名为{customer}的数据异常归因2')
        reason2 = []
        reason2_text = []
        # 归因2
        try:
            d_1_data = self.monitor1bystat_data.get_reason_2_data_by_stat_in_monitor1(trx_date=self.d_1_trx_date,
                                                                                      sales_name=sales_name,
                                                                                      stat_dispaysignedname=customer)
            d_2_data = self.monitor1bystat_data.get_reason_2_data_by_stat_in_monitor1(trx_date=self.d_2_trx_date,
                                                                                      sales_name=sales_name,
                                                                                      stat_dispaysignedname=customer)

            for d_2_item in d_2_data:
                d_2_success_amount = float(d_2_item['SUCCESS_AMOUNT'])
                if d_2_success_amount == 0:
                    continue
                d_1_success_amount = 0
                for d_1_item in d_1_data:
                    if (
                            d_1_item['PRODUCT'] == d_2_item['PRODUCT'] and
                            d_1_item['STAT_CUSTOMER_NO'] == d_2_item['STAT_CUSTOMER_NO']
                    ):
                        d_1_success_amount = float(d_1_item['SUCCESS_AMOUNT'])
                        break
                orig_scene = self.get_original_scene_by_merchant_no(
                    self.original_scene_dict,
                    d_2_item["STAT_CUSTOMER_NO"]
                )
                if abs(d_1_success_amount - d_2_success_amount) > 10000 and d_1_success_amount / d_2_success_amount - 1 > 1.5:
                    reason2.append(
                        f'归因二:商户签约名:{customer},商户编号:{d_2_item["STAT_CUSTOMER_NO"]},原始场景:{orig_scene},产品:{d_2_item["PRODUCT"]}，昨日交易金额{d_1_success_amount / 10000:.2f}万元，环比上升<text_tag color= green >{(d_1_success_amount / d_2_success_amount - 1) * 100:.2f}%</text_tag>')
                    reason2_text.append(
                        f'归因二:商户签约名:{customer},商户编号:{d_2_item["STAT_CUSTOMER_NO"]},原始场景:{orig_scene},产品:{d_2_item["PRODUCT"]}，昨日交易金额{d_1_success_amount / 10000:.2f}万元，环比上升{(d_1_success_amount / d_2_success_amount - 1) * 100:.2f}%')
                if abs(d_1_success_amount - d_2_success_amount) > 10000 and d_1_success_amount / d_2_success_amount - 1 < -0.5:
                    reason2.append(
                        f'归因二:商户签约名:{customer},商户编号:{d_2_item["STAT_CUSTOMER_NO"]},原始场景:{orig_scene},产品:{d_2_item["PRODUCT"]}，昨日交易金额{d_1_success_amount / 10000:.2f}万元，环比下降<text_tag color=  red  >{abs(d_1_success_amount / d_2_success_amount - 1) * 100:.2f}%</text_tag>')
                    reason2_text.append(
                        f'归因二:商户签约名:{customer},商户编号:{d_2_item["STAT_CUSTOMER_NO"]},原始场景:{orig_scene},产品:{d_2_item["PRODUCT"]}，昨日交易金额{d_1_success_amount / 10000:.2f}万元，环比下降{abs(d_1_success_amount / d_2_success_amount - 1) * 100:.2f}%')


        except Exception as e:
            print('归因2处理错误')

        return reason2, reason2_text

    def find_reason3(self, sales_name, customer) -> list:
        print(f'监控一处理{sales_name}的商户签约名为{customer}的数据异常归因3')
        reason3 = []
        reason3_text = []

        '''
        2、交易对手方交易环比波动异常
        归因③【商户签约名+付款方签约名】：
        - ([D-1]交易金额- [D-2]交易金额）的绝对值>=100000
        - 交易环比（[D-1]交易金额/[D-2]交易金额-1
          - >150%——上升
          - <-50%——下降
        '''
        # 归因3
        try:
            d_1_data = self.monitor1bystat_data.get_reason_3_data_by_stat_in_monitor1(trx_date=self.d_1_trx_date,
                                                                                      sales_name=sales_name,
                                                                                      stat_dispaysignedname=customer)
            d_2_data = self.monitor1bystat_data.get_reason_3_data_by_stat_in_monitor1(trx_date=self.d_2_trx_date,
                                                                                      sales_name=sales_name,
                                                                                      stat_dispaysignedname=customer)
            for d_2_item in d_2_data:
                d_2_success_amount = float(d_2_item['SUCCESS_AMOUNT'])
                if d_2_success_amount == 0:
                    continue
                d_1_success_amount = 0
                for d_1_item in d_1_data:
                    if d_1_item['PAYER_CUSTOMER_SIGNEDNAME'] == d_2_item['PAYER_CUSTOMER_SIGNEDNAME']:
                        d_1_success_amount = float(d_1_item['SUCCESS_AMOUNT'])
                        break
                if abs(d_1_success_amount - d_2_success_amount) > 100000 and d_1_success_amount / d_2_success_amount - 1 > 1.5:
                    reason3.append(
                        f'归因三:主要影响的付款方签约名:{d_2_item["PAYER_CUSTOMER_SIGNEDNAME"]}，昨日交易金额{d_1_success_amount / 10000:.2f}万元，环比上升<text_tag color=green>{d_1_success_amount / d_2_success_amount - 1:.2f}%</text_tag>')
                    reason3_text.append(
                        f'归因三:主要影响的付款方签约名:{d_2_item["PAYER_CUSTOMER_SIGNEDNAME"]}，昨日交易金额{d_1_success_amount / 10000:.2f}万元，环比上升{d_1_success_amount / d_2_success_amount - 1:.2f}%')
                if abs(d_1_success_amount - d_2_success_amount) > 100000 and d_1_success_amount / d_2_success_amount - 1 < -0.5:
                    reason3.append(
                        f'归因三:主要影响的付款方签约名:{d_2_item["PAYER_CUSTOMER_SIGNEDNAME"]}，昨日交易金额{d_1_success_amount / 10000:.2f}万元，环比下降<text_tag color=red>{abs(d_1_success_amount / d_2_success_amount - 1):.2f}%</text_tag>')
                    reason3_text.append(
                        f'归因三:主要影响的付款方签约名:{d_2_item["PAYER_CUSTOMER_SIGNEDNAME"]}，昨日交易金额{d_1_success_amount / 10000:.2f}万元，环比下降{abs(d_1_success_amount / d_2_success_amount - 1):.2f}%')


        except Exception as e:
            print('归因3处理错误')

        return reason3, reason3_text

# if __name__ == "__main__":
#     a = Monitor1ByStat()
#     b = a.run()
#     print(b)
