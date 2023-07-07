from typing import Literal

from pydantic import BaseModel

from model.base_mongodb import BaseMongoModel
from util.const_util import MONGO_DB_NAME


class User(BaseModel):
    username: str
    gmail: str
    password: str
    role: Literal['user', 'admin']
    is_ban: bool = None
    is_activate: bool = None

    class Config:
        schema_extra = {
            "example": {
                "username": "test",
                "gmail": 'test@gmail.com',
                "password": '123456',
                "role": 'user',
                "is_ban": False,
                "is_activate": True
            }
        }


class UserUpdate(User):
    password: str = None


class UserModel(BaseMongoModel):
    def __init__(self):
        super().__init__(MONGO_DB_NAME, 'User')
        self.collection.create_index('gmail', unique=True)
