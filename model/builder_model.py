import pymongo
from pydantic import BaseModel

from model.base_mongodb import BaseMongoModel
from util.const_util import MONGO_DB_NAME


class BuilderType(BaseModel):
    name: str


class BuilderValue(BaseModel):
    builder_type: str
    name: str
    image_src: str


class BuilderTypeModel(BaseMongoModel):
    def __init__(self):
        super().__init__(MONGO_DB_NAME, 'BuilderType')
        self.collection.create_index('name', unique=True)


class BuilderValueModel(BaseMongoModel):
    def __init__(self):
        super().__init__(MONGO_DB_NAME, 'BuilderValue')
        self.collection.create_index([('builder_type_id', pymongo.ASCENDING),
                                      ('name', pymongo.ASCENDING)],
                                     name='builder_type_id_name', unique=True)
