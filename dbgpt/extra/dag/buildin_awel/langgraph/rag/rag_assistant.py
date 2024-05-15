#! /usr/bin/env python3.8
import logging
import requests
import json
from typing import Dict
import aiohttp
import re
import os
from dbgpt.util import envutils

# const
TENANT_ACCESS_TOKEN_URI = "/open-apis/auth/v3/tenant_access_token/internal"
MESSAGE_URI = "/open-apis/im/v1/messages"
# RAG_FLOW_BASE_URL = "http://localhost:8066"
# RAG_FLOW_CHAT_TOKEN = "Bearer ragflow-Y0NDlmNTQ2MTEwMDExZWZiZTMzMDI0Mm"
# RAG_FLOW_BASE_URL = "http://172.31.91.206:8066"
# RAG_FLOW_CHAT_TOKEN = "Bearer ragflow-M4MDBhYmNjMDFlMDExZWZhYWY2MDI0Mm"
RAG_FLOW_BASE_URL = os.getenv('RAG_FLOW_BASE_URL')
RAG_FLOW_CHAT_TOKEN = os.getenv('RAG_FLOW_CHAT_TOKEN')


class RAGApiClient(object):
    def __init__(self):
        '''
            nothing
        '''

    async def test_slow_http(self, user_id):
        # https://httpbin.org/delay/10
        url = RAG_FLOW_BASE_URL + "/v1/api/new_conversation?name=" + user_id
        headers = {'Content-Type': 'application/json; charset=utf-8',
                   'Authorization': RAG_FLOW_CHAT_TOKEN}
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get('http://httpbin.org/delay/8') as response:
                print("Status:", response.status)
                print("Content-type:", response.headers['content-type'])

                html = await response.json()
                print("Body:", html, "...")
                return html

    async def async_coversation_start(self, user_id):
        headers = {'Content-Type': 'application/json; charset=utf-8',
                   'Authorization': RAG_FLOW_CHAT_TOKEN}
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(RAG_FLOW_BASE_URL + "/v1/api/new_conversation?name=" + user_id) as resp:
                print(resp.status)
                print(await resp.text())
                return resp

    async def async_chat(self, conversation_id, messages):
        headers = {'Content-Type': 'application/json; charset=utf-8',
                   'Authorization': RAG_FLOW_CHAT_TOKEN}
        data = {
            "conversation_id": conversation_id,
            "messages": messages,
        }

        print("rag start chat", conversation_id, messages, data)
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.post(RAG_FLOW_BASE_URL + "/v1/api/completion", data=data) as response:
                print(response.status)
                return response

    def coversation_start(self, user_id):
        url = RAG_FLOW_BASE_URL + "/v1/api/new_conversation?name=" + user_id
        headers = {'Content-Type': 'application/json; charset=utf-8',
                   'Authorization': RAG_FLOW_CHAT_TOKEN}
        data = {}
        resp = requests.request('GET', headers=headers, url=url, data=json.dumps(data), timeout=30)
        return resp

    def chat(self, conversation_id, messages):
        url = RAG_FLOW_BASE_URL + "/v1/api/completion"
        headers = {'Content-Type': 'application/json; charset=utf-8',
                   'Authorization': RAG_FLOW_CHAT_TOKEN}
        data = {
            "conversation_id": conversation_id,
            "messages": messages,
        }
        resp = requests.request('POST', headers=headers, url=url, data=json.dumps(data), timeout=30)
        return resp

    def get_image(self, image_id):
        url = RAG_FLOW_BASE_URL + "/v1/api/document/get/" + image_id
        headers = {'Content-Type': 'image/jpeg',
                   'Authorization': RAG_FLOW_CHAT_TOKEN}
        data = {}
        resp = requests.request('GET', headers=headers, url=url, data=json.dumps(data), timeout=30)
        return resp

    def single_round_chat(self, user_id, content):
        # res = await self.rag_api_client.async_coversation_start(user_id = open_id)
        res = self.coversation_start(user_id=user_id).json()
        id = res['data']['id']
        message_init = res['data']['message']
        new_message = {
            'content': content,
            'role': 'user'
        }
        message_init.append(new_message)

        origin_res = self.chat(conversation_id=id, messages=message_init).json()
        response = origin_res['data']['answer']
        chunks = origin_res['data']['reference']['chunks']

        # print("rag answer:",origin_res)
        pattern = r"##(.*?)\$\$"
        response = re.sub(pattern, "", response)
        # if '知识库中未找到您要的答案！' in response:
        #     message_api_client.send_text_with_open_id(open_id, main_text)
        #     return jsonify()

        cache_files = []
        reduce_count = 0
        for idx, chunk in enumerate(chunks):
            # print("current: ", chunk)
            if idx == 0:
                response += '\r\n---\r\n'

            name = chunk['docnm_kwd']
            # name = '产品能力全貌（标准）$$_$$老板管账$$_$$老板管账API接口能力梳理.pdf'
            names = name.split("$$_$$")
            file_name = names[len(names) - 1]
            if (file_name in cache_files) == True:
                reduce_count += 1
                continue
            cache_files.append(file_name)
            print(file_name, cache_files)
            if len(names) == 1:
                n = f"{idx + 1 - reduce_count}. {file_name}"
                response += n
                response += "\r\n"
                continue
            proj_path = os.getcwd()
            # print(os.path.join(proj_path,'dbgpt/extra/dag/buildin_awel/lark/static/ragfiles',names[0] + '.json'))
            f = open(os.path.join(proj_path, 'dbgpt/extra/dag/buildin_awel/lark/static/ragfiles', names[0] + '.json'))
            f_json = json.load(f)
            for key, value in f_json.items():
                if key == name:
                    f_metadata = json.loads(value)
                    n = f"[{idx + 1 - reduce_count}. {file_name}]({f_metadata['url']})"
                    response += n
                    response += "\r\n"
                    break
            # f_metadata = json.loads(f_json[name])
            # n = f"[{idx+1 - reduce_count}. {file_name}]({f_metadata['url']})"
            # n = file_name

        print('rag card response', response)
        return response, origin_res

    # end def

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
        msg_return = self.send("open_id", open_id, "interactive", content)
        return msg_return

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
        return resp

    def _authorize_tenant_access_token(self):
        # get tenant_access_token and set, implemented based on Feishu open api capability. doc link: https://open.feishu.cn/document/ukTMukTMukTM/ukDNz4SO0MjL5QzM/auth-v3/auth/tenant_access_token_internal
        url = "{}{}".format(self._lark_host, TENANT_ACCESS_TOKEN_URI)
        req_body = {"app_id": self._app_id, "app_secret": self._app_secret}
        response = requests.post(url, req_body)
        # response.to
        MessageApiClient._check_error_response(response)

        self._tenant_access_token = response.json().get("tenant_access_token")

    @staticmethod
    def _check_error_response(resp):
        # check if the response contains error information
        if resp.status_code != 200:
            print('feishu resp', resp.content)
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
