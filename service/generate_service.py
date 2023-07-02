from model.generate_model import GenerateModel
from service.base_service import BaseService
from service.user_service import UserService
from util.logger_util import logger
from util.langchain import llm, prompt

import json


class GenerateService(BaseService):
    def __init__(self):
        super().__init__(GenerateModel())

    def generate(self, payload):
        hint_text = payload.get('hint_text', '')

        result_gen = llm(prompt.format(subjects=hint_text))

        list_prompt_gen = []
        try:
            list_prompt_gen = list(json.loads(result_gen).values())
        except Exception as e:
            logger.error(e, result_gen)
            pass

        result = [prompt.strip() for prompt in list_prompt_gen]

        return result, 0, 'success'
