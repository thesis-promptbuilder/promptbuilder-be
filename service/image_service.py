import os
import uuid

from model.image_model import ImageModel
from service.base_service import BaseService
from service.user_service import UserService
from util import s3_image, pinecone_user_prompt
from util.time_util import get_time_string
from util.logger_util import logger
from util.error_util import Error
from util.const_util import AWS_CDN


class ImageService(BaseService):
    def __init__(self):
        super().__init__(ImageModel())

    def build_item(self, item):
        user_id = item.get('user_id', '')
        prompt = item.get('prompt', None)
        image = item.get('image', None)

        user, _, _ = UserService().get(user_id)
        if user is None:
            return None, -1, 'invalid user'

        file_name = ''
        if type(image) is dict:
            file_name = f'user/{user_id}/{get_time_string()}/{str(uuid.uuid1())}'
            if s3_image.upload_file(image["filename"], file_name):
                os.remove(image["filename"])
        else:
            file_name = f'user/{user_id}/{get_time_string()}/{str(uuid.uuid1())}'
            s3_image.put_object(image.file, file_name)

        image_src = f'/{file_name}'

        return {
            'user_id': user_id,
            'prompt': prompt,
            'image_src': image_src,
        }, 0, 'valid'

    def create(self, data):
        try:
            item, code, msg = self.build_item(data)
            if item is None:
                return None, code, msg
            prompt = item['prompt']

            logger.info(f'Build item: {msg}\n{item}')
            created_item, code, msg = self.model.create(item)
            # insert to pinecone
            if created_item:
                pinecone_user_prompt.upsert([created_item['id']],
                                            [prompt],
                                            [created_item])

            return created_item, code, msg
        except Exception as e:
            logger.error(e, exc_info=True)
            return None, Error.ERROR_CODE_GOT_EXCEPTION, e

    def create_many(self, items):
        try:
            valid_items = []
            for data in items:
                item, code, msg = self.build_item(data)
                logger.debug(f'Build item: {msg}\n{item}')
                if item:
                    valid_items.append(item)

            returned_items, code, msg = self.model.create_many(valid_items)

            if returned_items:
                pinecone_user_prompt.upsert([item['id'] for item in returned_items],
                                            [item['prompt'] for item in items],
                                            returned_items)
            return returned_items, code, msg
        except Exception as e:
            logger.error(e, exc_info=True)
            return None, Error.ERROR_CODE_GOT_EXCEPTION, e

    def get_extra_info(self, item):
        return {**item,
                'image_src': AWS_CDN + item['image_src']}
