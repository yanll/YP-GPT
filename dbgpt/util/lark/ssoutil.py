import json
import logging
from typing import Dict

import requests

from dbgpt.extra.cache.redis_cli import RedisClient
from dbgpt.util import envutils
from dbgpt.util.lark import larkutil

redis_client = RedisClient()


def get_sso_credential(open_id: str):

    if True:
        return envutils.getenv("SSO_TOKEN")

    url = envutils.getenv("PROC_CONSOLE_ENDPOINT") + '/auth/agent?openId=' + open_id

    credential = ""
    redis_key = "sso_credential_by_open_id_" + open_id
    try:
        credential: str = redis_client.get(redis_key)
    except Exception as e:
        logging.error("从缓存读取凭证信息失败：", e)
    if credential and credential != "":
        print("用户凭证信息缓存读取成功！", open_id)
        return credential
    else:
        larkutil.select_userinfo(open_id=open_id)
        resp = requests.request(method='POST', url=url, headers={}, params={}, data={})
        if resp.status_code != 200:
            logging.error("用户凭证接口异常：" + str(resp.status_code))
            return None
        result = resp.json()
        if result["code"] != 0:
            logging.error("飞书用户查询业务异常：" + resp.text)
            return None
        user = result['data']['user']
        userinfo = {
            "open_id": user['open_id'],
            "union_id": user['union_id'],
            "name": user['name'],
            "en_name": user['en_name'],
            "email": user['email'],
            "mobile": user['mobile']
        }
        redis_client.set(redis_key, json.dumps(userinfo), 30 * 60)
        print('\n用户详细信息返回结果：', userinfo)
        return userinfo
