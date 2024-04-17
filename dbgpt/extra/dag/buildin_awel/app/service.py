import logging
from typing import List

from dbgpt.extra.dag.buildin_awel.app.gpts_app_db import GptsAppDao

logger = logging.getLogger(__name__)


class GptsAppService:
    def __init__(self):
        self.gpts_app_dao = GptsAppDao()

    def get_gpts_app_list(self, team_mode: str = None) -> List:
        list = self.gpts_app_dao.get_gpts_app_list(team_mode)
        rs = []
        for row in list:
            rs.append({
                "app_code": row["app_code"],
                "app_name": row["app_describe"]
            })
        return rs
