import logging
import json
from typing import Optional
from dbgpt.util.json_utils import serialize

from ..base import Vis

logger = logging.getLogger(__name__)


class VisCalendar(Vis):

    async def display(self, **kwargs) -> Optional[str]:
        add_result = kwargs["add_result"]
        add_result_msg = "表格数据添加成功！" if add_result['code'] == 0 else "表格数据添加失败！"
        return (f"""
        紧急程度: {kwargs["content"].urgency}
        期望完成时间: {kwargs["content"].pre_time}
        \n
        执行结果：{add_result_msg}
        
        """ + "\n\n您的需求已提报至飞书文档：[需求收集](https://yeepay.feishu.cn/base/NorvbogbxaCD4VsMrLlcTzv0nTe?table=tblG1alED3YxCJua&view=vewj2nYdpi)，感谢使用！"
                )

    async def generate_param(self, **kwargs) -> Optional[str]:
        add_result = kwargs["add_result"]
        add_result_msg = "表格数据添加成功！" if add_result['code'] == 0 else "表格数据添加失败！"
        result = {
            "飞书执行结果": add_result_msg,
            "紧急程度": kwargs["content"].urgency,
            "期望完成时间": kwargs["content"].pre_time,
            "confirm": kwargs["content"].confirm,
            "ai_message": kwargs["content"].ai_message
        }
        return result

    @classmethod
    def vis_tag(cls):
        return "vis-calendar"
