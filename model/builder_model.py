import pymongo
from pydantic import BaseModel

from model.base_mongodb import BaseMongoModel
from util.const_util import MONGO_DB_NAME


class BuilderType(BaseModel):
    parent: str
    name: str
    short_name: str


class BuilderValue(BaseModel):
    parent: str
    name: str
    image_src: str


class BuilderTypeModel(BaseMongoModel):
    def __init__(self):
        super().__init__(MONGO_DB_NAME, 'BuilderType')
        self.collection.create_index([('parent', pymongo.ASCENDING),
                                      ('name', pymongo.ASCENDING)],
                                     name='parent_name', unique=True)


class BuilderValueModel(BaseMongoModel):
    def __init__(self):
        super().__init__(MONGO_DB_NAME, 'BuilderValue')
        self.collection.create_index([('parent', pymongo.ASCENDING),
                                      ('name', pymongo.ASCENDING)],
                                     name='parent_name', unique=True)
