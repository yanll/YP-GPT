"""Chat history database model."""
from typing import List

from sqlalchemy import text

from dbgpt.storage.metadata import BaseDao


class GptsAppDao(BaseDao):

    def get_gpts_app_list(self, team_mode: str = None) -> List:
        session = self.get_raw_session()
        result = session.execute(text("SELECT * FROM GPTS_APP where team_mode = :team_mode and (app_name like '%需求收集助手%' or app_name like '%会议室预定助手%')"), {'team_mode': team_mode})
        rs = []
        for row in result:
            dic = row._asdict()
            rs.append(dic)
        return rs
