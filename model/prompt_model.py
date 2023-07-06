from pydantic import BaseModel

from model.base_mongodb import BaseMongoModel
from util.config_util import mongodb_config


class Prompt(BaseModel):
    user_id: str
    prompt: str


class PromptModel(BaseMongoModel):
    def __init__(self):
        super().__init__(mongodb_config['db_name'], mongodb_config['prompt_collection'])
