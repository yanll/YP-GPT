import logging
from typing import Optional, Type

from langchain.tools import BaseTool
from langchain_core.callbacks import (
    CallbackManagerForToolRun,
)
from pydantic import BaseModel, Field

from dbgpt.extra.dag.buildin_awel.langgraph.rag.rag_assistant import RAGApiClient


class KnowledgeInput(BaseModel):
    """

    """
    conv_id: str = Field(
        name="conv_id",
        description="the value of conv_id",
    )
    question: str = Field(
        name="问题",
        description="问题",
        default=""
    )


class KnowledgeTool(BaseTool):
    name: str = "knowledge_tool"
    description: str = (
        "知识库问答工具，用于从易宝的知识库中检索答案并回复给用户。\n"
        "当询问“易宝”公司相关的业务知识、公司制度、企业文化、办公流程、办事流程、知识库搜索、产品、名词定义，以及寻找业务负责人、寻找解决方案等非常有用。\n"
        ""
    )
    args_schema: Type[BaseModel] = KnowledgeInput

    def _run(
            self,
            conv_id: str = "",
            question: str = "",
            run_manager: Optional[CallbackManagerForToolRun] = None
    ):
        print("开始运行知识问答工具：", conv_id, question)
        try:
            reuqires = []
            if question == "":
                reuqires.append("question")
            if len(reuqires) > 0:
                return {"success": "false", "response_message": "the description of " + "[" + ".".join(reuqires) + "]"}
            return handle(
                conv_id=conv_id,
                question=question
            )
        except Exception as e:
            logging.error("知识问答工具运行异常：" + conv_id + " " + question, e)
            return repr(e)


def handle(
        conv_id: str = "",
        question: str = ""
):
    print("发送知识问答结果卡片：", conv_id)
    try:
        rag_api_client = RAGApiClient()

        response, origin_res = rag_api_client.single_round_chat(user_id=conv_id, content=question)

        answer = response
        print("知识库调用结果：", conv_id, question, answer)

        return {
            "success": "true",
            "error_message": "",
            "action": {
                "action_name": "send_lark_form_card",
                "card_name": "knowledge_result"
            },
            "data": {
                "conv_id": conv_id,
                "question": question,
                "answer": answer
            }
        }
    except Exception as e:
        raise Exception("知识问答数据组装失败：" + conv_id + " " + question, e)
