from pydantic import BaseModel

from model.base_mongodb import BaseMongoModel
from util.const_util import MONGO_DB_NAME


class Image(BaseModel):
    user_id: str
    prompt: str
    image_src: str


class ImageModel(BaseMongoModel):
    def __init__(self):
        super().__init__(MONGO_DB_NAME, 'Image')
