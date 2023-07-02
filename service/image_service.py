from model.image_model import ImageModel
from service.base_service import BaseService
from service.prompt_service import PromptService
from service.user_service import UserService
from util import s3_image, sqs
from util.time_util import get_time_string
from util.logger_util import logger
from util.error_util import Error
from util.const_util import AWS_CDN


class ImageService(BaseService):
    def __init__(self):
        super().__init__(ImageModel())

    def build_item(self, item):
        user_id = item.get('user_id', '')
        user, _, _ = UserService().get(user_id)
        if user is None:
            return None, -1, 'invalid user'

        prompt_id = item.get('prompt_id', '')
        prompt, _, _ = PromptService().get(prompt_id)
        if prompt is None:
            return None, -1, 'invalid prompt'

        image = item.get('image', None)
        if image is None:
            return None, -1, 'invalid image'

        file_name = f'user/{user_id}/{get_time_string()}/{image.filename}'
        s3_image.put_object(image.file, file_name)

        image_src = f'/{file_name}'

        return {
            'user_id': user_id,
            'prompt_id': prompt_id,
            'image_src': image_src,
            'prompt': prompt.get('prompt', ''),
            'negative_prompt': prompt.get('negative_prompt', '')
        }, 0, 'valid'

    def create(self, data):
        try:
            item, code, msg = self.build_item(data)
            if item is None:
                return None, code, msg
            prompt = item.pop('prompt')
            negative_prompt = item.pop('negative_prompt')

            logger.info(f'Build item: {msg}\n{item}')
            created_item, code, msg = self.model.create(item)
            # add to sqs
            sqs.send_message({'id': created_item['id'],
                              'prompt_id': data['prompt_id'],
                              'user_id': data['user_id'],
                              'image_src': item['image_src'],
                              'prompt': prompt,
                              'negative_prompt': negative_prompt})
            return created_item, code, msg
        except Exception as e:
            logger.error(e, exc_info=True)
            return None, Error.ERROR_CODE_GOT_EXCEPTION, e

    def get_extra_info(self, item):
        return {**item,
                'image_src': AWS_CDN + item['image_src']}

    def get(self, id, _filter={}, deep=True):
        try:
            item, code, msg = self.model.get(id, _filter=_filter)
            if not item:
                return None, Error.ERROR_CODE_GOT_NO_SUCH_ITEM, Error.ERROR_MESSAGE_GOT_NO_SUCH_ITEM
            if deep:
                user_id = item.get('user_id', '')
                prompt_id = item.get('prompt_id', '')
                user, _, _ = UserService().get(user_id)
                prompt, _, _ = PromptService().get(prompt_id)

                item = {
                    **item,
                    'image_src': AWS_CDN + item['image_src'],
                    'user_gmail': user.get('gmail', ''),
                    'prompt': prompt.get('prompt', ''),
                    'negative_prompt': prompt.get('negative_prompt', '')
                }

            return item, code, msg
        except Exception as e:
            logger.error(e, exc_info=True)
            return None, Error.ERROR_CODE_GOT_EXCEPTION, e
