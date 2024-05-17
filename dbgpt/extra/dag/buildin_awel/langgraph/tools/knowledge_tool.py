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
        name="question",
        description="the value of question",
        default=""
    )
    ref: str = Field(
        name="ref",
        description="the value of ref",
        default=""
    )


class KnowledgeTool(BaseTool):
    name: str = "knowledge_tool"
    description: str = (
        "易宝问答工具，用于从易宝知识库中查询答案并回复给用户。\n"
        "可以回答和易宝相关的一切问题，当其他工具不匹配时优先调用此工具。\n"
        "当询问易宝相关的业务知识、公司制度、企业文化、办公流程、办事流程、知识库搜索、产品、名词定义，以及寻找业务负责人、寻找解决方案等优先调用此工具。\n"
        "当询问和易宝有关的内容时优先调用此工具。"
    )
    args_schema: Type[BaseModel] = KnowledgeInput

    def _run(
            self,
            conv_id: str = "",
            question: str = "",
            ref: str = "",
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
                question=question,
                ref=ref
            )
        except Exception as e:
            logging.error("知识问答工具运行异常：" + conv_id + " " + question, e)
            return repr(e)


def handle(
        conv_id: str = "",
        question: str = "",
        ref: str = ""
):
    print("发送知识问答结果卡片：", conv_id)
    try:
        rag_api_client = RAGApiClient()

        response, origin_res = rag_api_client.single_round_chat(user_id=conv_id, content=question)
        answer_from_knowledge = response
        answer_from_general_ai = ref
        answer = ""
        from_knowledge = "false"
        c_len = 0
        if "data" in origin_res:
            data = origin_res["data"]
            if "reference" in data:
                reference = data["reference"]
                c_len = reference["total"]
        if c_len > 0:
            from_knowledge = "true"
            answer = response
        else:
            answer = ref
        print("知识库调用结果：", conv_id, question, response)
        print("知识工具_AI引用：", ref)
        print("知识工具_知识引用：", answer_from_knowledge)
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
                "answer_from_knowledge": answer_from_knowledge,
                "answer_from_general_ai": ref,
                "answer": answer,
                "from_knowledge": from_knowledge
            }
        }
    except Exception as e:
        raise Exception("知识问答数据组装失败：" + conv_id + " " + question, e)
