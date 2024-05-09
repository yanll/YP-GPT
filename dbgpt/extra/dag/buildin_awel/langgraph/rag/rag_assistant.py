#! /usr/bin/env python3.8
import logging
import requests
import json
from typing import Dict
import aiohttp

# const
TENANT_ACCESS_TOKEN_URI = "/open-apis/auth/v3/tenant_access_token/internal"
MESSAGE_URI = "/open-apis/im/v1/messages"


class RAGApiClient(object):
    def __init__(self, rag_api_endpoint, rag_api_key):
        self.rag_api_endpoint = rag_api_endpoint
        self.rag_api_key = rag_api_key

    async def test_slow_http(self,user_id):
        # https://httpbin.org/delay/10
        url = "http://172.31.91.206:8066/v1/api/new_conversation?name="+user_id
        headers = {'Content-Type': 'application/json; charset=utf-8',
                   'Authorization': 'Bearer ragflow-M4MDBhYmNjMDFlMDExZWZhYWY2MDI0Mm'}
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get('http://httpbin.org/delay/8') as response:
                print("Status:", response.status)
                print("Content-type:", response.headers['content-type'])

                html = await response.json()
                print("Body:", html, "...")
                return html
    

    async def async_coversation_start(self,user_id):
        headers = {'Content-Type': 'application/json; charset=utf-8',
                   'Authorization': 'Bearer ragflow-M4MDBhYmNjMDFlMDExZWZhYWY2MDI0Mm'}
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get("http://172.31.91.206:8066/v1/api/new_conversation?name="+user_id) as resp:
                print(resp.status)
                return await resp.json()
            
    
    async def async_chat(self,conversation_id, messages):
        headers = {'Content-Type': 'application/json; charset=utf-8',
                   'Authorization': 'Bearer ragflow-M4MDBhYmNjMDFlMDExZWZhYWY2MDI0Mm'}
        data = {
            "conversation_id": conversation_id,
            "messages": messages,
        }
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.post("http://172.31.91.206:8066/v1/api/completion",data=data) as response:
                print(response.status)
                return await response.json()
    
    def coversation_start(self,user_id):
        url = "http://172.31.91.206:8066/v1/api/new_conversation?name="+user_id
        headers = {'Content-Type': 'application/json; charset=utf-8',
                   'Authorization': 'Bearer ragflow-M4MDBhYmNjMDFlMDExZWZhYWY2MDI0Mm'}
        data = {}
        resp = requests.request('GET', headers=headers, url=url, data=json.dumps(data))
        return resp

    def chat(self,conversation_id, messages):
        url = "http://172.31.91.206:8066/v1/api/completion"
        headers = {'Content-Type': 'application/json; charset=utf-8',
                   'Authorization': 'Bearer ragflow-M4MDBhYmNjMDFlMDExZWZhYWY2MDI0Mm'}
        data = {
            "conversation_id": conversation_id,
            "messages": messages,
        }
        resp = requests.request('POST', headers=headers, url=url, data=json.dumps(data))
        return resp

    def get_image(self,image_id):
        url = "http://172.31.91.206:8066/v1/api/document/get/"+image_id
        headers = {'Content-Type': 'image/jpeg',
                   'Authorization': 'Bearer ragflow-M4MDBhYmNjMDFlMDExZWZhYWY2MDI0Mm'}
        data = {}
        resp = requests.request('GET', headers=headers, url=url, data=json.dumps(data))
        return resp

    @staticmethod
    def _check_error_response(resp):
        # check if the response contains error information
        if resp.status_code != 200:
            resp.raise_for_status()
        response_dict = resp.json()
        code = response_dict.get("code", -1)
        if code != 0:
            logging.error(response_dict)
            raise LarkException(code=code, msg=response_dict.get("msg"))


class MessageApiClient(object):
    def __init__(self, app_id, app_secret, lark_host):
        self._app_id = app_id
        self._app_secret = app_secret
        self._lark_host = lark_host
        self._tenant_access_token = ""

    @property
    def tenant_access_token(self):
        return self._tenant_access_token

    def send_text_with_open_id(self, open_id, content):
        self.send("open_id", open_id, "interactive", content)

    def send(self, receive_id_type, receive_id, msg_type, content):
        # send message to user, implemented based on Feishu open api capability. doc link: https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message/create
        self._authorize_tenant_access_token()
        url = "{}{}?receive_id_type={}".format(
            self._lark_host, MESSAGE_URI, receive_id_type
        )
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": "Bearer " + self.tenant_access_token,
        }
        req_body = {
            "receive_id": receive_id,
            "content": json.dumps(content),
            "msg_type": msg_type,
        }
        resp = requests.post(url=url, headers=headers, json=req_body)
        MessageApiClient._check_error_response(resp)

    def _authorize_tenant_access_token(self):
        # get tenant_access_token and set, implemented based on Feishu open api capability. doc link: https://open.feishu.cn/document/ukTMukTMukTM/ukDNz4SO0MjL5QzM/auth-v3/auth/tenant_access_token_internal
        url = "{}{}".format(self._lark_host, TENANT_ACCESS_TOKEN_URI)
        req_body = {"app_id": self._app_id, "app_secret": self._app_secret}
        response = requests.post(url, req_body)
        MessageApiClient._check_error_response(response)
        self._tenant_access_token = response.json().get("tenant_access_token")

    @staticmethod
    def _check_error_response(resp):
        # check if the response contains error information
        if resp.status_code != 200:
            resp.raise_for_status()
        response_dict = resp.json()
        code = response_dict.get("code", -1)
        if code != 0:
            logging.error(response_dict)
            raise LarkException(code=code, msg=response_dict.get("msg"))


class LarkException(Exception):
    def __init__(self, code=0, msg=None):
        self.code = code
        self.msg = msg

    def __str__(self) -> str:
        return "{}:{}".format(self.code, self.msg)

    __repr__ = __str__
