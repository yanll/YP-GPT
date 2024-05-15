#! /usr/bin/env python3.8
import logging
import uuid
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


# const
TENANT_ACCESS_TOKEN_URI = "/open-apis/auth/v3/tenant_access_token/internal"
MESSAGE_URI = "/open-apis/im/v1/messages"

APP_ID = envutils.getenv('LARK_RAG_APP_ID')
APP_SECRET = envutils.getenv('LARK_RAG_APP_SECRET')
VERIFICATION_TOKEN = envutils.getenv('LARK_RAG_VERIFICATION_TOKEN')
ENCRYPT_KEY = ""
LARK_HOST = "https://open.feishu.cn"

message_api_client = MessageApiClient(APP_ID, APP_SECRET, LARK_HOST)


class RAGLarkHandler:
    def __init__(self, **kwargs):
        self.app_chat_service = AppChatService()
        self.rag_api_client = RAGApiClient()
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
            req_text_content = json.loads(text_content)['text']
            
             # 发送loading卡片
            message_id = lark_message_util.send_loading_message_rag(receive_id=open_id)
            
              # 初始化ragflow的对话后，先存起来消息信息
            self.app_chat_service.add_app_chat_his_message({
                "id": str(uuid.uuid1()),
                "agent_name": "RAG",
                "node_name": "start",
                "conv_uid": open_id,
                "message_type": "human",
                "content": req_text_content,
                "message_detail": json.dumps(input_body),
                "display_type": "rag_card",
                "lark_message_id": ""
            })
            
            
            response, origin_res = self.rag_api_client.single_round_chat(user_id=open_id, content=req_text_content)
            
            # 更新loading卡片
            lark_message_util.update_loading_message_rag(message_id=message_id)
            
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
                "message_detail": json.dumps(origin_res),
                "display_type": "rag_card",
                "lark_message_id": resp['message_id']
            })

        except Exception as e:
            lark_message_util.update_loading_message_rag(message_id=message_id, type='error')
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
        