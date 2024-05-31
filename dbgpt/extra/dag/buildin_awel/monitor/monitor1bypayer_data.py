from dbgpt.extra.dag.buildin_awel.monitor.airline_monitor_data_provider import AirlineMonitorDataProvider


class Monitor1ByPayerDataProvider(AirlineMonitorDataProvider):
    def __init__(self):
        super().__init__()

    def get_data_by_payer_in_monitor1(self, trx_date: str, payer_sales_name=None, payer_customer_signedname=None):
        parameters = {
            "TRX_DATE": trx_date
        }
        if payer_sales_name:
            parameters['PAYER_SALES_NAME'] = payer_sales_name
        if payer_customer_signedname:
            parameters['PAYER_CUSTOMER_SIGNEDNAME'] = payer_customer_signedname

        try:
            resp = self.dmall_client.post(
                api_name="get_data_by_payer_in_montor1",
                parameters=parameters
            )
            resp = resp.json()
            data = resp['data']['data']
        except Exception as e:
            print('监控一获取数据异常')
            raise e

        return data

    def get_industry_line_data_by_payer_in_monitor1(self, trx_date: str):
        try:
            resp = self.dmall_client.post(
                api_name="get_industry_line_data_by_payer_in_montor1",
                parameters={
                    'TRX_DATE': trx_date
                }
            )
            resp = resp.json()
            data = resp['data']['data']
        except Exception as e:
            print('监控一获取数据异常')
            raise e

        return data

    def get_reason_4_data_by_payer_in_monitor1(self, trx_date: str, payer_sales_name: str,
                                               payer_customer_signedname: str):
        try:
            resp = self.dmall_client.post(
                api_name="get_reason_4_data_by_payer_in_montor1",
                parameters={
                    'TRX_DATE': trx_date,
                    'PAYER_SALES_NAME': payer_sales_name,
                    'PAYER_CUSTOMER_SIGNEDNAME': payer_customer_signedname
                }
            )
            resp = resp.json()
            data = resp['data']['data']
        except Exception as e:
            print('监控一归因四获取数据异常')
            raise e

        return data

    def get_reason_5_data_by_payer_in_monitor1(self, trx_date: str, payer_sales_name: str,
                                               payer_customer_signedname: str):
        try:
            resp = self.dmall_client.post(
                api_name="get_reason_5_data_by_payer_in_montor1",
                parameters={
                    'TRX_DATE': trx_date,
                    'PAYER_SALES_NAME': payer_sales_name,
                    'PAYER_CUSTOMER_SIGNEDNAME': payer_customer_signedname
                }
            )
            resp = resp.json()
            data = resp['data']['data']
        except Exception as e:
            print('监控一归因四获取数据异常')
            raise e

        return data
