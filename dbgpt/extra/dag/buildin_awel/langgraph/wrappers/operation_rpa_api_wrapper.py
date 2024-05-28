
import json
import logging

import requests

from dbgpt.util import envutils, consts
from dbgpt.util.lark import ssoutil

logger = logging.getLogger(__name__)
logger.setLevel("INFO")
BASE_URL = envutils.getenv("RPA_SERVER_ENDPOINT")
ACCESSKEY_ID = envutils.getenv("RPA_SERVER_ACCESSKEY_ID")
ACCESSKEY_SCRET = envutils.getenv("RPA_SERVER_ACCESSKEY_SECRET")

_SCHEDULEUUID_DICT = {
    'GET_OPR_STATUS': '',
    'OPEN_BAIDU': '98b6a511-2a86-4a0e-8e66-998aeb6954db',
}

def get_rpa_token() -> str:
    url = f"{BASE_URL}/oapi/token/v2/token/create?accessKeyId={ACCESSKEY_ID}&accessKeySecret={ACCESSKEY_SCRET}"
    headers = {}
    payload = {}
    logger.info("开始获取RPA TOKEN")
    response = requests.request("GET", url, headers=headers, data=payload)
    try:
        resp = response.json()
        if resp.get('code') != 200:
            raise Exception("获取token失败：" + str(resp.msg))
        
        # return '跨境行业线'
        logger.info(f"RPA TOKEN: {resp['data']['accessToken']}")
        return resp['data']['accessToken']

    except Exception as e:
        logger.error("获取token失败：" + str(e))
        raise e


def execute_rpa_task(task: str):
    url = f"{BASE_URL}/oapi/dispatch/v2/task/start"
    
    if _SCHEDULEUUID_DICT.get(task) is None:
        raise Exception("Task not found.")
    
    payload = json.dumps({
        "scheduleUuid": _SCHEDULEUUID_DICT[task]
    })

    try:
        # 获取token
        token = get_rpa_token()
        headers = {
            'Authorization': f"Bearer {token}",
            'Content-Type': 'application/json',
        }
        response = requests.request("POST", url, headers=headers, data=payload)

        res_json = response.json()
        
        if res_json['code'] != 200:
            raise Exception(f"执行任务失败，task：{task}, msg: {res_json['msg']}")
        
        return res_json
    except Exception as e:
        logging.error(e)