import requests
import logging
import json
import datetime

def get_past_working_days(working_days):
    current_date = datetime.datetime.now().date()
    current_date = str(current_date - datetime.timedelta(days=1))
    url = f"http://ycenc.yeepay.com:8606/holiday/get_last_weekdays_by_date?date={current_date}&days={working_days}"
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'app_key': "ai-assistants",
        'app_secret': "fcd2f6kd0c3acf1c"
    }
    logging.info("开始调用：%s", url)
    resp = requests.request('GET', headers=headers, url=url, data={}, timeout=(5, 10))

    data_list = json.loads(resp.text)['data']
    return data_list



