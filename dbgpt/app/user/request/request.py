from dbgpt._private.pydantic import BaseModel


class UserQueryRequest(BaseModel):
    username: str
    email: str
