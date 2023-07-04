from model.prompt_model import PromptModel
from model.upvote_model import UpvoteModel
from service.base_service import BaseService
from service.user_service import UserService
from util.logger_util import logger
from util.error_util import Error


class PromptService(BaseService):
    def __init__(self):
        super().__init__(PromptModel())
