from dbgpt.extra.dag.buildin_awel.monitor.monitor1bypayer_data import Monitor1ByPayerDataProvider
from dbgpt.extra.dag.buildin_awel.monitor.monitor1bystat_data import Monitor1ByStatDataProvider
from dbgpt.extra.dag.buildin_awel.monitor.monitor2_data import Monitor2DataProvider
from dbgpt.extra.dag.buildin_awel.monitor.monitor3_data import Monitor3DataProvider
from dbgpt.extra.dag.buildin_awel.monitor.monitor4_data import Monitor4DataProvider


class AirlineMonitorDataHandler:
    def __init__(self):
        self.monitor1bypayer_data = Monitor1ByPayerDataProvider()
        self.monitor1bystat_data = Monitor1ByStatDataProvider()
        self.monitor2_data = Monitor2DataProvider()
        self.monitor3_data = Monitor3DataProvider()
        self.monitor4_data = Monitor4DataProvider()

    def get_past_working_days(self, working_days):
        return self.get_past_working_days(working_days)
