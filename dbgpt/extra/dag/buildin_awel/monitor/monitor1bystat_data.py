from dbgpt.extra.dag.buildin_awel.monitor.airline_monitor_data import AirlineMonitorDataProvider


class Monitor1ByStatDataProvider(AirlineMonitorDataProvider):
    def __init__(self):
        super().__init__()

    def get_data_by_stat_in_monitor1(self, trx_date: str, sales_name=None, stat_dispaysignedname=None):
        parameters = {
            "TRX_DATE": trx_date
        }
        if sales_name:
            parameters['SALES_NAME'] = sales_name
        if stat_dispaysignedname:
            parameters['STAT_DISPAYSIGNEDNAME'] = stat_dispaysignedname
        try:
            resp = self.dmall_client.post(
                api_name="get_data_by_stat_in_montor1",
                parameters=parameters
            )
            resp = resp.json()
            data = resp['data']['data']
        except Exception as e:
            print('监控一获取数据异常')
            raise e

        return data

    def get_industry_line_data_by_stat_in_monitor1(self, trx_date: str):
        try:
            resp = self.dmall_client.post(
                api_name="get_industry_line_data_by_stat_in_montor1",
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

    def get_reason_1_data_by_stat_in_monitor1(self, trx_date: str, sales_name: str, stat_dispaysignedname: str):
        try:
            resp = self.dmall_client.post(
                api_name="get_reason_1_data_by_stat_in_montor1",
                parameters={
                    'TRX_DATE': trx_date,
                    'SALES_NAME': sales_name,
                    'STAT_DISPAYSIGNEDNAME': stat_dispaysignedname
                }
            )
            resp = resp.json()
            data = resp['data']['data']
        except Exception as e:
            print('监控一归因一获取数据异常')
            raise e

        return data

    def get_reason_2_data_by_stat_in_monitor1(self, trx_date: str, sales_name: str, stat_dispaysignedname: str):
        try:
            resp = self.dmall_client.post(
                api_name="get_reason_2_data_by_stat_in_montor1",
                parameters={
                    'TRX_DATE': trx_date,
                    'SALES_NAME': sales_name,
                    'STAT_DISPAYSIGNEDNAME': stat_dispaysignedname
                }
            )
            resp = resp.json()
            data = resp['data']['data']
        except Exception as e:
            print('监控一归因二获取数据异常')
            raise e

        return data

    def get_reason_3_data_by_stat_in_monitor1(self, trx_date: str, sales_name: str, stat_dispaysignedname: str):
        try:
            resp = self.dmall_client.post(
                api_name="get_reason_3_data_by_stat_in_montor1",
                parameters={
                    'TRX_DATE': trx_date,
                    'SALES_NAME': sales_name,
                    'STAT_DISPAYSIGNEDNAME': stat_dispaysignedname
                }
            )
            resp = resp.json()
            data = resp['data']['data']
        except Exception as e:
            print('监控一归因三获取数据异常')
            raise e

        return data
