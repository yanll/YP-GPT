from dbgpt.extra.dag.buildin_awel.monitor.airline_monitor_data_provider import AirlineMonitorDataProvider


class Monitor2DataProvider(AirlineMonitorDataProvider):
    def __init__(self):
        super().__init__()

    def get_data_by_stat_in_monitor2(self, trx_date: str, sales_name=None, stat_dispaysignedname=None):
        parameters = {
            'TRX_DATE': trx_date
        }
        if sales_name:
            parameters['SALES_NAME'] = sales_name
        if stat_dispaysignedname:
            parameters['STAT_DISPAYSIGNEDNAME'] = stat_dispaysignedname
        try:
            resp = self.dmall_client.post(
                api_name="get_data_by_stat_in_montor2",
                parameters=parameters
            )
            resp = resp.json()
            data = resp['data']['data']
        except Exception as e:
            print('监控二获取数据异常')
            raise e

        return data

    def get_data_by_payer_in_monitor2(self, trx_date: str, payer_sales_name=None, payer_customer_signedname=None):
        parameters = {
            'TRX_DATE': trx_date
        }
        if payer_sales_name:
            parameters['PAYER_SALES_NAME'] = payer_sales_name
        if payer_customer_signedname:
            parameters['PAYER_CUSTOMER_SIGNEDNAME'] = payer_customer_signedname
        try:
            resp = self.dmall_client.post(
                api_name="get_data_by_payer_in_montor2",
                parameters=parameters
            )
            resp = resp.json()
            data = resp['data']['data']
        except Exception as e:
            print('监控二获取数据异常')
            raise e

        return data
