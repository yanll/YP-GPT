from dbgpt._private.pydantic import BaseModel


class UserQueryResponse(BaseModel):
    id: int = None
    username: str = None
    email: str = None
