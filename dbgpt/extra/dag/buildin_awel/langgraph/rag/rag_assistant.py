#! /usr/bin/env python3.8
import logging
import requests
import json
from typing import Dict
import aiohttp
import re
import os
from dbgpt.util import envutils
from dbgpt.util.lark import lark_message_util, lark_card_util
import time

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
            "stream":False,
            "quote":True
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


    def single_round_chat(self, user_id, content, response_v='stale'):
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
        response = None
        if response_v == 'stale':
            response = generate_rag_response_card_stale(origin_res=origin_res)
        else:
            response = generate_rag_response_card(origin_res=origin_res)
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
    
    
    def update(self, message_id, content):
        # send message to user, implemented based on Feishu open api capability. doc link: https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message/create
        self._authorize_tenant_access_token()
        url = "{}{}/{}".format(
            self._lark_host, MESSAGE_URI, message_id
        )
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": "Bearer " + self.tenant_access_token,
        }
        req_body = {
            "content": json.dumps(content),
        }
        resp = requests.patch(url=url, headers=headers, json=req_body)
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


def generate_rag_response_card(origin_res):
    """
    Purpose: rag消息回复模板（拼接版本）
    """
    res_card = {
        "config": {},
        "i18n_elements": {
            "zh_cn": [
                {
                    "tag": "markdown",
                    "content": "test",
                    "text_align": "left",
                    "text_size": "normal"
                }
            ]
        },
        "i18n_header": {}
    }
    response = origin_res['data']['answer']
    chunks = origin_res['data']['reference']['doc_aggs']
    
    pattern = r"##(.*?)\$\$"
    matches = re.findall(pattern, response)
    response = re.sub(pattern, "", response)
    
    res_card["i18n_elements"]['zh_cn'][0]['content'] = response
    
    matches = list(dict.fromkeys(matches))
    
    cache_files = []
    reduce_count = 0
    for idx, chunk in enumerate(chunks):
                
        name = chunk['doc_name']
        # name = '产品能力全貌（标准）$$_$$老板管账$$_$$老板管账API接口能力梳理.pdf'
        names = name.split("$$_$$")
        file_name = names[len(names) - 1]
        
        # 根据文件名分类，并且存起来对应的img_id
        need_continue = False
        for cfile in cache_files:
            if cfile['name'] == file_name:
                reduce_count += 1
                cfile['imgs'].append(chunk['img_id'] if ('img_id' in chunk) else '')
                cfile['chunks_content'].append(chunk['content_ltks'] if ('content_ltks' in chunk) else None)
                need_continue = True
        if need_continue == True:
            continue
            
        file_dict = {
            'name': file_name,
            # 'imgs': [chunk['img_id']],
            'imgs': [chunk['img_id']]  if 'img_id' in chunk else [],
            # 'chunks_content':[chunk['content_ltks']],
            'chunks_content':[chunk['content_ltks']] if 'content_ltks' in chunk else [],
            'url': ''
        }
        
        # print(file_name,cache_files)
        print("参考文件名：",names)
        if len(names) == 1 :
            cache_files.append(file_dict)
            continue
        
        # 打开json文件，获取文件对应的飞书URL
        try:
            proj_path = os.getcwd()
            file_path = os.path.join(proj_path,'dbgpt/extra/dag/buildin_awel/lark/static/ragfiles',names[0] + '.json')
            f = open(file_path)
            print("查找源文件路径",file_path)
            f_json = json.load(f)
            for key, value in f_json.items():
                if key == name:
                    f_metadata = json.loads(value)
                    file_dict["url"] = f_metadata['url']
                    if f_metadata.get('file_type') is not None and f_metadata['file_type'] == 'feishu_doc':
                        file_dict['name'] = remove_file_extension(file_dict['name'])
                    break
            cache_files.append(file_dict)
        except Exception as e:
            print("can't find file",e)


    # if len(cache_files) > 0:
    #     res_card['i18n_elements']['zh_cn'].append()
    
    # startTime = time.time()
    
    # 分割线
    if len(cache_files) > 0:
        res_card['i18n_elements']['zh_cn'].append({
                "tag": "hr"
        })
        
    # 参考文档
    
    ref_mkd = ''
    for idx,f in enumerate(cache_files):
        # ref_mkd += res_card['i18n_elements']['zh_cn'].append(generate_collapsible_panel(f,idx+1))
        ref_mkd += generate_collapsible_panel(f,idx+1)
        ref_mkd += "\r\n"
        
    ref_shcema = {
                    "tag": "markdown",
                    "content": ref_mkd,
                    "text_align": "left",
                    "text_size": "normal"
                }
    res_card['i18n_elements']['zh_cn'].append(ref_shcema)
    # endTime = time.time()
    # howMuchTime = endTime - startTime
    
    # print("上传图片花费时间",str(howMuchTime) + " sec")
    
    res_card['i18n_elements']['zh_cn'].append(card_footer_template())
        
    
    return res_card
    
# end def


def generate_collapsible_panel(file,idx=0):
    # 富文本链接形式
    if file['url']:
        return "[{}. {}]({})".format(idx, file['name'],file['url'])
    else:
        return "{}. {}".format(idx, file['name'])
    """
    Purpose: 生成单个折叠面板 折叠+图片版本
    """
    panel_title = None
    panel_content = ''
    if file['url']:
        panel_title = "<link icon='file-link-docx-shortcut_outlined' url='{0}' pc_url='{1}' ios_url='' android_url=''>{2}</link>".format(file['url'],file['url'],file['name'])
    else:
        panel_title = "<link icon='file-link-docx-shortcut_outlined' url='{0}' pc_url='{1}' ios_url='' android_url=''>{2}</link>".format(file['url'],file['url'],file['name'])
        
    count = 0
    for i, img_id in enumerate(file['imgs']):  # looping through row
        # comment: 
        if bool(img_id):
            count += 1
            url = RAG_FLOW_BASE_URL + '/v1/document/image/' + img_id
            img_id = lark_message_util.upload_img_to_lark_by_url(url)
            panel_content += "![{}]({})".format(file['chunks_content'][i], img_id)
            
        else:
            panel_content += file['chunks_content'][i]
           
    print('上传图片数量：', count) 

        
    # end for
    return  {
      "tag": "collapsible_panel",
      "expanded": False,
      "header": {
        "title": {
          "tag": "markdown",
          "content": panel_title
        },
        "vertical_align": "center",
        "icon": {
            "tag": "standard_icon",
            "token": "down-small-ccm_outlined",
            "color": "",
            "size": "16px 16px"
        },
        "icon_position": "right",
        "icon_expanded_angle": -180
      },
    #   "border": {
    #     "color": "grey",
    #     "corner_radius": "5px"
    #   },
      "vertical_spacing": "8px",
      "padding": "8px 8px 8px 8px",
      "elements": [
        {
          "tag": "markdown",
          "content": panel_content
        }
      ]
    }
# end def

def generate_rag_response_card_stale(origin_res):
    """
    Purpose: 生成rag消息回复模板 (卡片模板版本)
    """
    response = origin_res['data']['answer']
    chunks = origin_res['data']['reference']['chunks']
    
    pattern = r"##(.*?)\$\$"
    response = re.sub(pattern, "", response)
    
    # print("rag answer:",origin_res)
    # if '知识库中未找到您要的答案！' in response:
    #     message_api_client.send_text_with_open_id(open_id, main_text)
    #     return jsonify()

    cache_files = []
    reduce_count = 0
    for idx, chunk in enumerate(chunks):
        # print("current: ", chunk)
        if idx == 0 :
            response += '\r\n---\r\n'
        
        name = chunk['docnm_kwd']
        # name = '产品能力全貌（标准）$$_$$老板管账$$_$$老板管账API接口能力梳理.pdf'
        names = name.split("$$_$$")
        file_name = names[len(names) - 1]
        if (file_name in cache_files) == True:
            reduce_count += 1
            continue
        cache_files.append(file_name)
        print(file_name,cache_files)
        if len(names) == 1 :
            n = f"{idx+1 - reduce_count}. {file_name}"
            response += n
            response += "\r\n"
            continue
        proj_path = os.getcwd()
        # print(os.path.join(proj_path,'dbgpt/extra/dag/buildin_awel/lark/static/ragfiles',names[0] + '.json'))
        f = open(os.path.join(proj_path,'dbgpt/extra/dag/buildin_awel/lark/static/ragfiles',names[0] + '.json'))
        f_json = json.load(f)
        for key, value in f_json.items():
            if key == name:
                f_metadata = json.loads(value)
                n = f"[{idx+1 - reduce_count}. {file_name}]({f_metadata['url']})"
                response += n
                response += "\r\n"
                break
        # f_metadata = json.loads(f_json[name])
        # n = f"[{idx+1 - reduce_count}. {file_name}]({f_metadata['url']})"
        # n = file_name
        
    print('rag card response', response) 
    return response
  
# end def

def card_footer_template():
    """
    Purpose: 
    """
    return {
            "tag": "column_set",
            "flex_mode": "none",
            "background_style": "default",
            "horizontal_spacing": "8px",
            "horizontal_align": "left",
            "columns": [
                {
                    "tag": "column",
                    "width": "weighted",
                    "vertical_align": "top",
                    "vertical_spacing": "8px",
                    "background_style": "default",
                    "elements": [
                        {
                            "tag": "button",
                            "text": {
                                "tag": "plain_text",
                                "content": ""
                            },
                            "type": "primary_text",
                            "complex_interaction": True,
                            "width": "default",
                            "size": "medium",
                            "icon": {
                                "tag": "standard_icon",
                                "token": "add-bold_outlined"
                            },
                            "hover_tips": {
                                "tag": "plain_text",
                                "content": "新会话"
                            },
                            "value": {
                                "event_type": "new_chat_rag"
                            }
                        }
                    ],
                    "weight": 5
                },
                {
                    "tag": "column",
                    "width": "weighted",
                    "vertical_align": "top",
                    "vertical_spacing": "8px",
                    "background_style": "default",
                    "elements": [
                        {
                            "tag": "button",
                            "text": {
                                "tag": "plain_text",
                                "content": ""
                            },
                            "type": "primary_text",
                            "complex_interaction": False,
                            "width": "fill",
                            "size": "medium",
                            "icon": {
                                "tag": "standard_icon",
                                "token": "thumbsup_outlined"
                            },
                            "value": {
                                "event_type": "like"
                            }
                        }
                    ],
                    "weight": 1
                },
                {
                    "tag": "column",
                    "width": "weighted",
                    "vertical_align": "top",
                    "vertical_spacing": "8px",
                    "background_style": "default",
                    "elements": [
                        {
                            "tag": "button",
                            "text": {
                                "tag": "plain_text",
                                "content": ""
                            },
                            "type": "primary_text",
                            "complex_interaction": True,
                            "width": "fill",
                            "size": "medium",
                            "icon": {
                                "tag": "standard_icon",
                                "token": "thumbdown_outlined"
                            },
                            "value": {
                                "event_type": "unlike_rag",
                                "event_source": "rag_standard_response",
                                "event_data": {
                                    "message": "产品助手提问"
                                }
                            }
                        }
                    ],
                    "weight": 1
                }
            ],
            "margin": "16px 0px 0px 0px"
          }
# end def


def remove_file_extension(filename):
    return os.path.splitext(filename)[0]