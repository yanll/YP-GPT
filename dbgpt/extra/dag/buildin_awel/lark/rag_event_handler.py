#! /usr/bin/env python3.8
import logging
import time
import uuid
import re
import json
from typing import Dict

from dbgpt.extra.dag.buildin_awel.app.service import AppChatService
from dbgpt.extra.dag.buildin_awel.langgraph.rag.rag_assistant import MessageApiClient
from dbgpt.extra.dag.buildin_awel.langgraph.rag.rag_assistant import RAGApiClient
import copy
from dbgpt.util import envutils
import asyncio
from dbgpt.util.lark import lark_message_util, lark_card_util
from dbgpt.extra.dag.buildin_awel.lark import card_templates

import os

# const
TENANT_ACCESS_TOKEN_URI = "/open-apis/auth/v3/tenant_access_token/internal"
MESSAGE_URI = "/open-apis/im/v1/messages"

APP_ID = envutils.getenv('LARK_RAG_APP_ID')
APP_SECRET = envutils.getenv('LARK_RAG_APP_SECRET')
VERIFICATION_TOKEN = envutils.getenv('LARK_RAG_VERIFICATION_TOKEN')
ENCRYPT_KEY = ""
LARK_HOST = "https://open.feishu.cn"
# rag_api_endpoint = "http://172.31.91.206:8066/v1/api/"
# rag_api_key = "ragflow-dhN2M4NzFhMDBiNzExZWY5NGY0MDI0Mm"
rag_api_endpoint = "https://demo.ragflow.io/v1/api/"
rag_api_key = "ragflow-c0NGJmZTVhMDEzMTExZWZiN2NhMDI0Mm"

message_api_client = MessageApiClient(APP_ID, APP_SECRET, LARK_HOST)


class RAGLarkHandler:
    def __init__(self, **kwargs):
        self.app_chat_service = AppChatService()
        self.rag_api_client = RAGApiClient(rag_api_endpoint, rag_api_key)
        super().__init__(**kwargs)

    async def handle(self, input_body: Dict):

        # res = await self.rag_api_client.test_slow_http()
        # print("result ", res)
        # return
        try:
            # comment: 
            sender_id = input_body['event']['sender']['sender_id']
            message = input_body['event']['message']
            if message['message_type'] != "text":
                logging.warn("Other types of messages have not been processed yet")
                return
            open_id = sender_id['open_id']
            text_content = message['content']
            
              # 初始化ragflow的对话后，先存起来消息信息
            self.app_chat_service.add_app_chat_his_message({
                "id": str(uuid.uuid1()),
                "agent_name": "RAG",
                "node_name": "start",
                "conv_uid": open_id,
                "message_type": "human",
                "content": json.loads(text_content)['text'],
                "message_detail": json.dumps(input_body),
                "display_type": "rag_card",
                "lark_message_id": ""
            })
            
            # res = await self.rag_api_client.async_coversation_start(user_id = open_id)
            res = self.rag_api_client.coversation_start(user_id=open_id).json()
            id = res['data']['id']
            message_init = res['data']['message']
            new_message = {
                'content': json.loads(text_content)['text'],
                'role': 'user'
            }
            message_init.append(new_message)
            
          
            
            res = self.rag_api_client.chat(conversation_id=id, messages=message_init).json()
            response = res['data']['answer']
            chunks = res['data']['reference']['chunks']
            
            print("rag answer:",res)
            
            # response = response.replace("##", "[").replace("$$", "]")
            pattern = r"##(.*?)\$\$"
            response = re.sub(pattern, "", response)

            # if '知识库中未找到您要的答案！' in response:
            #     message_api_client.send_text_with_open_id(open_id, main_text)
            #     return jsonify()
        
            cache_files = []
            for idx, chunk in enumerate(chunks):
                print("current: ", chunk)
                if idx == 0 :
                    response += '\r\n---'
                
                response += '\r\n'
                name = chunk['docnm_kwd']
                names = name.split("$$_$$")
                file_name = names[len(names) - 1]
                if (file_name in cache_files) == True:
                    continue
                cache_files.append(file_name)
                print(file_name,cache_files)
                if len(names) == 1 :
                    n = f"{idx+1}. {file_name}"
                    response += n
                    continue
                cur_dir_path = os.getcwd()
                print(os.path.join(cur_dir_path,'dbgpt/extra/dag/buildin_awel/lark/static/ragfiles',names[0] + '.json'))
                f = open(os.path.join(cur_dir_path,'dbgpt/extra/dag/buildin_awel/lark/static/ragfiles',names[0] + '.json'))
                f_json = json.load(f)
                f_metadata = json.loads(f_json[name])
                n = f"[{idx+1}. {file_name}]({f_metadata['url']})"
                response += n
                
            
            
            resp = lark_message_util.send_card_message_rag(
                    receive_id=open_id,
                    content=card_templates.create_rag_card_content.standard_response(
                        template_variable={
                            'content':response,
                            "unlike_callback_event": {
                                "event_type": "unlike_rag",
                                "event_source": "rag_standard_response",
                                "event_data": {
                                    "message": "产品助手提问"
                                }
                            }
                        }
                    )
                )
            
            # print("send rag card resp:" , resp)
            
            self.app_chat_service.add_app_chat_his_message({
                "id": str(uuid.uuid1()),
                "agent_name": "RAG",
                "node_name": "start",
                "conv_uid": open_id,
                "message_type": "ai",
                "content": response,
                "message_detail": json.dumps(res),
                "display_type": "rag_card",
                "lark_message_id": resp['message_id']
            })

        except Exception as e:
            resp = lark_message_util.send_card_message_rag(
                receive_id=open_id,
                content=card_templates.create_rag_card_content.standard_response(
                    template_variable={
                        'content':"系统错误，请联系管理员。",
                        "unlike_callback_event": {
                            "event_type": "unlike_rag",
                            "event_source": "rag_standard_response",
                            "event_data": {
                                "message": "产品助手提问"
                            }
                        }
                    }
                )
            )
            raise e
        # end try
        

