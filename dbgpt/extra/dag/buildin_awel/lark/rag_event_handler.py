#! /usr/bin/env python3.8
import logging
import requests
import json
from typing import Dict
from dbgpt.extra.dag.buildin_awel.langgraph.rag.rag_assistant import MessageApiClient
from dbgpt.extra.dag.buildin_awel.langgraph.rag.rag_assistant import RAGApiClient
import copy
from dbgpt.util import envutils

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
        self.rag_api_client = RAGApiClient(rag_api_endpoint, rag_api_key)
        super().__init__(**kwargs)

    async def handle(self, input_body: Dict):

        # res = await self.rag_api_client.test_slow_http()
        # print("result ", res)
        # return
        sender_id = input_body['event']['sender']['sender_id']
        message = input_body['event']['message']
        if message['message_type'] != "text":
            logging.warn("Other types of messages have not been processed yet")
            return
        open_id = sender_id['open_id']
        text_content = message['content']
        # res = await self.rag_api_client.async_coversation_start(user_id = open_id)
        res = self.rag_api_client.coversation_start(user_id = open_id).json()
        id = res['data']['id']
        message_init = res['data']['message']
        new_message = {
            'content':json.loads(text_content)['text'],
            'role':'user'
        }
        message_init.append(new_message)
        # res = await self.rag_api_client.async_chat(conversation_id = id,messages = message_init)
        res = self.rag_api_client.chat(conversation_id = id,messages = message_init).json()
        response = res['data']['answer']
        chunks = res['data']['reference']['chunks']
        # document_name = []
        # translation_table = str.maketrans(reference_number_replace)
        # response = response.translate(translation_table)
        response = response.replace("##","[").replace("$$","]")
        main_text = {
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
                                "tag": "markdown",
                                "content": response,
                                "text_align": "left",
                                "text_size": "normal"
                            }
                        ],
                        "weight": 1
                    }
                ],
                "margin": "16px 0px 0px 0px"
        }
        # if '知识库中未找到您要的答案！' in response:
        #     message_api_client.send_text_with_open_id(open_id, main_text)
        #     return jsonify()
        reference_template = {
            "tag": "collapsible_panel",  # 折叠面板的标签。
            "expanded": False,  # 面板是否展开。默认值 false。
            "background_color": "grey",  # 折叠面板的背景色，默认为透明
            "header": {
                # 折叠面板的标题设置。
                "title": {
                    # 标题文本设置。支持 plain_text 和 markdown。
                    "tag": "markdown",
                    "content": "**参考**",
                },
                "vertical_align": "center",  # 标题区的垂直居中方式。
                "padding": "4px 0px 4px 8px",  # 标题区的内边距。
                "icon": {
                    # 标题前缀图标
                    "tag": "standard_icon",  # 图标类型.
                    "token": "arrange_outlined",  # 图标库中图标的 token。当 tag 为 standard_icon 时生效。
                    "color": "blue",  # 图标的颜色。当 tag 为 standard_icon 时生效。
                    "img_key": "img_v2_38811724",  # 自定义前缀图标的图片 key。当 tag 为 custom_icon 时生效。
                    "size": "16px 16px",  # 图标的尺寸。默认值为 10px 10px。
                },
                "icon_position": "follow_text",  # 图标的位置。默认值为 right。
                "icon_expanded_angle": -180,  # 折叠面板展开时图标旋转的角度，正值为顺时针，负值为逆时针。默认值为 180。
            },
            "border": {
                # 边框设置。默认不显示边框。
                "color": "grey",  # 边框的颜色。
                "corner_radius": "5px",  # 圆角设置。
            },
            "vertical_spacing": "8px",  # 面板内元素垂直边距设置。默认值为 8px。
            "padding": "8px 8px 8px 8px",  # 内容区的内边距。
            "elements": [
                # # 此处可添加各个组件的 JSON 结构。暂不支持表单（form）组件。
                # {
                #     "tag": "markdown",
                #     "content": "similarity",
                # },
                {
                    "tag": "markdown",
                    "content": "refer_text",
                }

            ],
        }
        i = 0
        card = []
        card.append(main_text)
        ref_text = {
                    "tag": "markdown",
                    "content": "similarity",
                }
        doc_aggs = res['data']['reference']['doc_aggs']
        for chunk in chunks:
            # print("current: ", chunk)
            temp = copy.deepcopy(reference_template)
            # if(chunk['docnm_kwd'].endswith("pdf")):
            #     # print(chunk['positions'])
            #     # temp['header']['title']['content'] = "["+str(i+1)+"] "+chunk['docnm_kwd'] + " 第" + str((int)(chunk['positions'][0][0])) +"页"
            #     temp['header']['title']['content'] = "[" + str(i + 1) + "] " + chunk['docnm_kwd']
            #     dic_id = chunk['doc_id']
            #     print(dic_id)
            #     document = rag_api_client.get_image(dic_id)
            #     print(document)
            # else:
            #     temp['header']['title']['content'] = "[" + str(i + 1) + "] " + chunk['docnm_kwd']
            name = chunk['docnm_kwd']
            temp['header']['title']['content'] = "[" + str(i) + "] " + name
            ref_text_sim = copy.deepcopy(ref_text)
            ref_text_self = copy.deepcopy(ref_text)
            # ref_text_sim['content'] = str(chunk['similarity'])
            ref_text_self['content'] = chunk['content_with_weight']
            temp['elements'] = [ref_text_self]
            card.append(temp)
            i = i+1

        content = {
            "config": {},
            "i18n_elements": {
                "zh_cn": card
            },
            "i18n_header": {}
        }
        
        # print(f"response card {card}")
        message_api_client.send_text_with_open_id(open_id, content)
        # # message_api_client.send_text_with_open_id(open_id, content2)
        # return jsonify()


    async def debug_handle(self, input_body: Dict):

        # res = await self.rag_api_client.test_slow_http()
        # print("result ", res)
        # return
        sender_id = input_body['event']['sender']['sender_id']
        message = input_body['event']['message']
        if message['message_type'] != "text":
            logging.warn("Other types of messages have not been processed yet")
            return
        open_id = sender_id['open_id']
        text_content = message['content']
        res = await self.rag_api_client.async_coversation_start(user_id = open_id)
        # res = self.rag_api_client.coversation_start(user_id = open_id).json()

        print("res",res)
        return
        id = res['data']['id']
        message_init = res['data']['message']
        new_message = {
            'content':json.loads(text_content)['text'],
            'role':'user'
        }
        message_init.append(new_message)
        # res = await self.rag_api_client.async_chat(conversation_id = id,messages = message_init)
        res = self.rag_api_client.chat(conversation_id = id,messages = message_init).json()

        response = res['data']['answer']
        chunks = res['data']['reference']['chunks']
        # document_name = []
        # translation_table = str.maketrans(reference_number_replace)
        # response = response.translate(translation_table)
        response = response.replace("##","[").replace("$$","]")
        main_text = {
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
                                "tag": "markdown",
                                "content": response,
                                "text_align": "left",
                                "text_size": "normal"
                            }
                        ],
                        "weight": 1
                    }
                ],
                "margin": "16px 0px 0px 0px"
        }
        # if '知识库中未找到您要的答案！' in response:
        #     message_api_client.send_text_with_open_id(open_id, main_text)
        #     return jsonify()
        reference_template = {
            "tag": "collapsible_panel",  # 折叠面板的标签。
            "expanded": False,  # 面板是否展开。默认值 false。
            "background_color": "grey",  # 折叠面板的背景色，默认为透明
            "header": {
                # 折叠面板的标题设置。
                "title": {
                    # 标题文本设置。支持 plain_text 和 markdown。
                    "tag": "markdown",
                    "content": "**参考**",
                },
                "vertical_align": "center",  # 标题区的垂直居中方式。
                "padding": "4px 0px 4px 8px",  # 标题区的内边距。
                "icon": {
                    # 标题前缀图标
                    "tag": "standard_icon",  # 图标类型.
                    "token": "arrange_outlined",  # 图标库中图标的 token。当 tag 为 standard_icon 时生效。
                    "color": "blue",  # 图标的颜色。当 tag 为 standard_icon 时生效。
                    "img_key": "img_v2_38811724",  # 自定义前缀图标的图片 key。当 tag 为 custom_icon 时生效。
                    "size": "16px 16px",  # 图标的尺寸。默认值为 10px 10px。
                },
                "icon_position": "follow_text",  # 图标的位置。默认值为 right。
                "icon_expanded_angle": -180,  # 折叠面板展开时图标旋转的角度，正值为顺时针，负值为逆时针。默认值为 180。
            },
            "border": {
                # 边框设置。默认不显示边框。
                "color": "grey",  # 边框的颜色。
                "corner_radius": "5px",  # 圆角设置。
            },
            "vertical_spacing": "8px",  # 面板内元素垂直边距设置。默认值为 8px。
            "padding": "8px 8px 8px 8px",  # 内容区的内边距。
            "elements": [
                # # 此处可添加各个组件的 JSON 结构。暂不支持表单（form）组件。
                # {
                #     "tag": "markdown",
                #     "content": "similarity",
                # },
                {
                    "tag": "markdown",
                    "content": "refer_text",
                }

            ],
        }
        i = 0
        card = []
        card.append(main_text)
        ref_text = {
                    "tag": "markdown",
                    "content": "similarity",
                }
        doc_aggs = res['data']['reference']['doc_aggs']
        for chunk in chunks:
            # print("current: ", chunk)
            temp = copy.deepcopy(reference_template)
            # if(chunk['docnm_kwd'].endswith("pdf")):
            #     # print(chunk['positions'])
            #     # temp['header']['title']['content'] = "["+str(i+1)+"] "+chunk['docnm_kwd'] + " 第" + str((int)(chunk['positions'][0][0])) +"页"
            #     temp['header']['title']['content'] = "[" + str(i + 1) + "] " + chunk['docnm_kwd']
            #     dic_id = chunk['doc_id']
            #     print(dic_id)
            #     document = rag_api_client.get_image(dic_id)
            #     print(document)
            # else:
            #     temp['header']['title']['content'] = "[" + str(i + 1) + "] " + chunk['docnm_kwd']
            name = chunk['docnm_kwd']
            temp['header']['title']['content'] = "[" + str(i) + "] " + name
            ref_text_sim = copy.deepcopy(ref_text)
            ref_text_self = copy.deepcopy(ref_text)
            # ref_text_sim['content'] = str(chunk['similarity'])
            ref_text_self['content'] = chunk['content_with_weight']
            temp['elements'] = [ref_text_self]
            card.append(temp)
            i = i+1

        content = {
            "config": {},
            "i18n_elements": {
                "zh_cn": card
            },
            "i18n_header": {}
        }
        
        # print(f"response card {card}")
        message_api_client.send_text_with_open_id(open_id, content)
        # # message_api_client.send_text_with_open_id(open_id, content2)
        # return jsonify()
