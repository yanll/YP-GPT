from dbgpt.extra.dag.buildin_awel.monitor.airline_monitor_data_provider import AirlineMonitorDataProvider
from dbgpt.extra.dag.buildin_awel.monitor.monitor1bypayer_data import Monitor1ByPayerDataProvider
from dbgpt.extra.dag.buildin_awel.monitor.monitor1bystat_data import Monitor1ByStatDataProvider
from dbgpt.extra.dag.buildin_awel.monitor.monitor2_data import Monitor2DataProvider
from dbgpt.extra.dag.buildin_awel.monitor.monitor3_data import Monitor3DataProvider
from dbgpt.extra.dag.buildin_awel.monitor.monitor4_data import Monitor4DataProvider


class AirlineMonitorDataHandler:
    def __init__(self):
        self.airline_monitor_data_provider = AirlineMonitorDataProvider()
        self.monitor1bypayer_data = Monitor1ByPayerDataProvider()
        self.monitor1bystat_data = Monitor1ByStatDataProvider()
        self.monitor2_data = Monitor2DataProvider()
        self.monitor3_data = Monitor3DataProvider()
        self.monitor4_data = Monitor4DataProvider()

    def get_past_working_days(self, working_days):
        return self.airline_monitor_data_provider.get_past_working_days(working_days)

    def get_original_scene_dict(self):
        dict_list = self.airline_monitor_data_provider.get_original_scene_dict_list()
        rs = {}
        for rec in dict_list:
            rs[rec['CUSTOMER']] = rec["SCENE"]
        return rs

    def get_original_scene_by_merchant_no(self, scene_dict: dict, merchant_no: str) -> str:
        if scene_dict is None:
            return ""
        if merchant_no is None or merchant_no == "":
            return ""
        if merchant_no in scene_dict:
            return scene_dict[merchant_no]
        return "-"
