import logging
import json
from typing import Optional

from ..base import Vis

logger = logging.getLogger(__name__)


class VisDemand(Vis):
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
