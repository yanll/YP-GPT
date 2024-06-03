import datetime
import json
import logging

import requests

from dbgpt.util import envutils
from dbgpt.util.dmallutil import DmallClient


class AirlineMonitorDataProvider:
    def __init__(self):
        self.dmall_client = DmallClient()

    def get_original_scene_dict_list(self):
        try:
            resp = self.dmall_client.post(
                api_name="air_original_scene",
                parameters={

                }
            )
            resp = resp.json()
            data = resp['data']['data']
            return data
        except Exception as e:
            print('原始场景字典获取数据异常')
            raise e

    def get_past_working_days(self, working_days):
        current_date = datetime.datetime.now().date()
        current_date = str(current_date - datetime.timedelta(days=1))
        endpoint = envutils.getenv("AI_ASSISTANTS_ENDPOINT")
        url = f"{endpoint}/holiday/get_last_weekdays_by_date?date={current_date}&days={working_days}"
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'app_key': "ai-assistants",
            'app_secret': "fcd2f6kd0c3acf1c"
        }
        logging.info("开始调用：%s", url)
        resp = requests.request('GET', headers=headers, url=url, data={}, timeout=(5, 10))

        data_list = json.loads(resp.text)['data']
        return data_list