from typing import Dict

import requests
import json

from dbgpt.util import envutils, consts


class DmallClient:
    def post(
            self,
            api_name: str,
            parameters: Dict,
            api_version: str = "V1.0",
            endpoint: str = envutils.getenv("DMALL_ENDPOINT")
    ):
        print("\n商店调用: ", api_name, " ", parameters)
        url = endpoint + "/dataapi/output/postapi/" + api_name
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        data = {
            "appname": "app",
            "appkey": envutils.getenv("DMALL_SK"),
            "version": api_version,
            "parameters": parameters
        }
        resp = requests.request('POST', headers=headers, url=url, data=json.dumps(data),
                                timeout=(5, 15))
        print("商店调用返回结果：", resp.text)
        return resp

# client = DmallClient()
# rs = client.post(
#     api_name="query_merchant_info",
#     parameters={
#         "CUSTOMERNUMBER": "10012982662"
#     }
# )
# print(rs)
