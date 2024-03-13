from sqlalchemy import Column, Integer, String

from dbgpt._private.config import Config
from dbgpt.storage.metadata import BaseDao, Model

CFG = Config()


class UserEntity(Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(64))
    email = Column(String(64))

    def __repr__(self):
        return f"UserEntity(id={self.id}, username='{self.username}', email='{self.email}')"


class UserDao(BaseDao):

    def get_user(self, query: UserEntity):
        session = self.get_raw_session()
        users = session.query(UserEntity)
        result = users.all()
        session.close()
        return result
