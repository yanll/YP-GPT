import json
import logging
import os
import uuid
from dbgpt.client import Client
from datetime import datetime
from dbgpt.util.nl2sql import nl2sql_card

import asyncio


class Nl2sqlAssistant:
    def __init__(self):
        pass

    async def handle(
            self,
            input: str,
            conv_uid: str = ""
    ):
        # Use the tool.
        print("数据分析助手开始调用模型：")

        try:
            # 根据用户输入信息获取数据库内容
            DBGPT_API_KEY = "dbgpt"
            DB_NAME = "bigdata_ai"

            client = Client(api_key=DBGPT_API_KEY)
            res = await client.chat(
                messages=input,
                model="proxyllm",
                chat_mode="chat_data",
                chat_param=DB_NAME
            )
            rs = res.choices[0].message.content

            return rs
        except Exception as e:
            logging.error("数据分析助手运行异常：", e)
            raise e


async def chat_test():
    nl2sql_assistant = Nl2sqlAssistant()
    rs = await nl2sql_assistant.handle("各行业的销售毛利，用环形图表示", "")
    print(rs)


if __name__ == '__main__':
    asyncio.run(
        chat_test()
    )



