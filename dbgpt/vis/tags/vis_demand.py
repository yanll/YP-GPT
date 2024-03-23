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
        con = kwargs["content"].json()
        result = {
            "title": "默认标题",
            "内求内容": kwargs["content"].demand,
            "紧急程度": kwargs["content"].urgency,
            "期望完成时间": kwargs["content"].pre_time,
            "thought": kwargs["content"].thought,
            "data": kwargs["data_df"],
            "content": con
        }
        return result

    @classmethod
    def vis_tag(cls):
        return "vis-demand"
