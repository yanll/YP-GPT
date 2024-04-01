import logging
import json
from typing import Optional
from dbgpt.util.json_utils import serialize

from ..base import Vis

logger = logging.getLogger(__name__)


class VisDemand(Vis):

    async def display(self, **kwargs) -> Optional[str]:
        return f"```{self.vis_tag()}\n{json.dumps(await self.generate_param(**kwargs), default=serialize, ensure_ascii=False)}\n```"

    async def generate_param(self, **kwargs) -> Optional[str]:
        add_result = kwargs["add_result"]
        add_result_msg = "表格数据添加成功！" if add_result['code'] == 0 else "表格数据添加失败！"
        result = {
            "飞书执行结果": add_result_msg,
            "需求内容": kwargs["content"].demand,
            "紧急程度": kwargs["content"].urgency,
            "期望完成时间": kwargs["content"].pre_time,
            "confirm": kwargs["content"].confirm,
            "ai_message": kwargs["content"].ai_message
        }
        return result

    @classmethod
    def vis_tag(cls):
        return "vis-demand"
