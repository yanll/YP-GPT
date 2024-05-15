import logging
from typing import Optional, Type

from langchain.tools import BaseTool
from langchain_core.callbacks import (
    CallbackManagerForToolRun,
)
from pydantic import BaseModel, Field

from dbgpt.extra.dag.buildin_awel.lark import card_templates
from dbgpt.util.lark import larkutil, lark_card_util, lark_message_util


class FeedbackCollectInput(BaseModel):
    """
    我要反馈一个问题：
    -详细内容：文件下载速度太慢
    -影响范围：运营使用体验很差
    -建议：建议优化下载速度
    -参考文档：
    """
    conv_id: str = Field(
        name="conv_id",
        description="the value of conv_id",
    )
    feedback: str = Field(
        name="反馈/吐槽的内容详情",
        description="反馈/吐槽的内容详情",
        default=""
    )
    effect: str = Field(
        name="影响范围",
        description="影响范围",
        default=""
    )
    recommendation: str = Field(
        name="recommendation",
        description="意见建议",
        default=""
    )
    reference_url: str = Field(
        name="参考文档链接",
        description="参考文档链接",
        default=""
    )


class FeedbackCollectTool(BaseTool):
    name: str = "feedback_collect_tool"
    description: str = (
        "问题反馈工具\n"
        "请注意：\n"
        "1、当需要吐槽或提交问题、反馈、意见、建议时非常有用。\n"
        "2、调用本工具需要的参数值来自用户输入，可以默认为空，但是禁止随意编造。\n"
        ""
    )
    args_schema: Type[BaseModel] = FeedbackCollectInput

    def _run(
            self,
            conv_id: str = "",
            feedback: str = "",
            effect: str = "",
            recommendation: str = "",
            reference_url: str = ""
    ):
        print("开始运行问题反馈收集工具：", conv_id, feedback)
        try:
            reuqires = []
            if feedback == "":
                reuqires.append("feedback")
            if len(reuqires) > 0:
                s = str(reuqires)
                return {"success": "false", "response_message": "the description of " + str(reuqires)}
            return handle(
                conv_id=conv_id,
                feedback=feedback,
                effect=effect,
                recommendation=recommendation,
                reference_url=reference_url
            )
        except Exception as e:
            logging.error("问题反馈收集工具运行异常：" + conv_id + " " + feedback, e)
            return repr(e)


def handle(
        conv_id: str = "",
        feedback: str = "",
        effect: str = "",
        recommendation: str = "",
        reference_url: str = ""
):
    try:
        return {
            "success": "true",
            "error_message": "",
            "action": {
                "action_name": "send_lark_form_card",
                "card_name": "feedback_collect"
            },
            "data": {
                "conv_id": conv_id,
                "feedback": feedback,
                "effect": effect,
                "recommendation": recommendation,
                "reference_url": reference_url
            }
        }
    except Exception as e:
        raise Exception("问题反馈数据组装失败：" + conv_id + " " + feedback, e)
