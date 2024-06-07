from dbgpt.extra.dag.buildin_awel.monitor.airline_monitor_data_provider import AirlineMonitorDataProvider


class Monitor4DataProvider(AirlineMonitorDataProvider):
    def __init__(self):
        super().__init__()

    def get_data_by_stat_in_monitor4(self, trx_date: str, sales_name=None, stat_dispaysignedname=None, payer=None):
        parameters = {
            'TRX_DATE': trx_date
        }
        if sales_name:
            parameters['SALES_NAME'] = sales_name
        if stat_dispaysignedname:
            parameters['STAT_DISPAYSIGNEDNAME'] = stat_dispaysignedname
        if payer:
            parameters['PAYER_DISPAYSIGNEDNAME'] = payer
        try:
            resp = self.dmall_client.post(
                api_name="get_data_by_stat_in_montor4",
                parameters=parameters
            )
            resp = resp.json()
            data = resp['data']['data']
        except Exception as e:
            print('监控四获取数据异常')
            raise e

        return data
