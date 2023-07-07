import pymongo
from pydantic import BaseModel

from model.base_mongodb import BaseMongoModel
from util.const_util import MONGO_DB_NAME


class Upvote(BaseModel):
    user_sender_id: str
    user_receiver_id: str
    image_id: str


class UpvoteModel(BaseMongoModel):
    def __init__(self):
        super().__init__(MONGO_DB_NAME, 'Upvote')
        self.collection.create_index([('user_sender_id', pymongo.ASCENDING),
                                      ('user_receiver_id', pymongo.ASCENDING),
                                      ('image_id', pymongo.ASCENDING)],
                                     name='sender_receiver_image', unique=True)
