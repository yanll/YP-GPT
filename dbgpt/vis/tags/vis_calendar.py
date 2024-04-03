import logging
import json
from typing import Optional
from dbgpt.util.json_utils import serialize

from ..base import Vis

logger = logging.getLogger(__name__)


class VisCalendar(Vis):

    async def display(self, **kwargs) -> Optional[str]:
        return (f"""
            执行结果：{kwargs}
            """)

    async def generate_param(self, **kwargs) -> Optional[str]:
        result = {
            "content": kwargs["content"].content
        }
        return result

    @classmethod
    def vis_tag(cls):
        return "vis-calendar"
