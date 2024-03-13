import logging
from enum import Enum

from dbgpt._private.config import Config
from dbgpt.app.user.request.response import (
    UserQueryResponse
)
from dbgpt.app.user.user_db import UserDao, UserEntity

user_dao = UserDao()

logger = logging.getLogger(__name__)
CFG = Config()


class SyncStatus(Enum):
    TODO = "TODO"
    FAILED = "FAILED"
    RUNNING = "RUNNING"
    FINISHED = "FINISHED"


class UserService:
    def __init__(self):
        pass

    def get_user(self):
        query = UserEntity(
            username=None, email=None
        )
        users = user_dao.get_user(query)
        responses = []
        for user in users:
            res = UserQueryResponse()
            res.id = user.id
            res.username = user.username
            res.email = user.email
            responses.append(res)
        return responses
