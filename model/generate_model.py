from pydantic import BaseModel

from model.base_mongodb import BaseMongoModel
from util.const_util import MONGO_DB_NAME


class Generate(BaseModel):
    user_id: str
    hint_text: str
    result: list


class GenerateModel(BaseMongoModel):
    def __init__(self):
        super().__init__(MONGO_DB_NAME, 'Generate')
