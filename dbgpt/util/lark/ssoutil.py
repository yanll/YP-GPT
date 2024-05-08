import json
import logging
from typing import Dict

import requests

from dbgpt.extra.cache.redis_cli import RedisClient
from dbgpt.util import envutils
from dbgpt.util.lark import larkutil, aesutil

redis_client = RedisClient()


def get_sso_credential(open_id: str):
    url = envutils.getenv("PROC_CONSOLE_ENDPOINT") + '/auth/agent?openId=' + open_id

    credential = ""
    redis_key = "sso_credential_by_open_id_" + open_id
    try:
        credential: str = redis_client.get(redis_key)
    except Exception as e:
        logging.error("从缓存读取凭证信息失败：", e)
    if credential and credential != "":
        print("用户凭证信息缓存读取成功！", open_id, credential, "END")
        return credential
    try:
        userinfo = larkutil.select_userinfo(open_id=open_id)
        data = {
            "en_name": userinfo["en_name"],
            "name": userinfo["name"],
            "email": userinfo["email"],
            "mobile": userinfo["mobile"],
        }
        logging.info("飞书用户：" + str(data))
        resp = requests.request(
            method='POST',
            url=url,
            headers={
                "Content-Type": "application/json; charset=utf-8"
            },
            params={}, data=json.dumps(data))

        if resp.status_code != 200:
            logging.error("用户凭证接口异常：" + str(resp.status_code))
            return None
        text = resp.text
        logging.info("UIA用户：" + text)

        dict = json.loads(text)
        code = dict['code']
        if code != "200":
            logging.error("UIA用户查询业务异常：" + resp.text)
            return None
        data = dict['data']
        credential = aesutil.decrypt_from_base64(envutils.getenv("AES_KEY"), data)
        # redis_client.set(redis_key, credential, 5 * 60)
        print('\n用户凭证信息结果：', data)
        print("\n用户凭证信息结果！", open_id, credential, "END")

        return credential
    except Exception as e:
        logging.error("用户凭证解析异常：", open_id)
        raise Exception("用户凭证解析异常", e)
