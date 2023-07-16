from model.user_model import UserModel
from service.base_service import BaseService
from util.logger_util import logger
from util.error_util import Error
from util.const_util import MAILTRAP_KEY

import random
import mailtrap as mt

MAX_USERNAME = 20


class UserService(BaseService):
    def __init__(self):
        super().__init__(UserModel())

    def build_update_item(self, update_item):
        item = {}
        item['username'] = update_item.get('username', None)
        item['gmail'] = update_item.get('gmail', None)
        item['password'] = update_item.get('password', None)
        item['role'] = update_item.get('role', None)
        item['is_ban'] = update_item.get('is_ban', None)
        item['is_activate'] = update_item.get('is_activate', None)

        return item, '0', 'item valid'

    def update_user(self, id, data):
        try:
            data.pop('create_time', None)
            data.pop('update_time', None)
            item = {}
            item['username'] = data.get('username', '')
            item = {k: v for k, v in item.items() if v is not None}

            update_count, code, msg = self.model.update(id, item=item)
            if update_count:
                item, _, _ = self.get(id)
                return item, code, msg
            return None, -1, 'None of item was updated'
        except Exception as e:
            logger.error(e, exc_info=True)
            return None, Error.ERROR_CODE_GOT_EXCEPTION, e

    def signup(self, data):
        username = data.get('username', None)
        gmail = data.get('gmail', None)
        password = data.get('password', None)
        verify_code = random.randint(100000, 999999)

        if not (username and gmail and password):
            return None, -1, 'invalid data'

        mail = mt.Mail(
            sender=mt.Address(email="mailtrap@promptbuilder.pro",
                              name="PromptBuilder"),
            to=[mt.Address(email=gmail)],
            subject="PromptBuilder Verify Code",
            text=str(verify_code),
        )

        client = mt.MailtrapClient(token=MAILTRAP_KEY)
        client.send(mail)

        result, code, msg = self.model.create({
            'username': username[:MAX_USERNAME],
            'gmail': gmail,
            'password': password,
            'role': 'user',
            'is_ban': False,
            'is_activate': False,
            'verify_code': verify_code
        })

        return result, code, msg

    def extend_delete(self, ids):
        from service.image_service import ImageService
        image_service = ImageService()

        list_image, _, _, _ = image_service.get_list(
            {'user_id': {'$in': ids}}, size=1000000)

        result, code, msg = image_service.delete_many(
            ids=[image['id'] for image in list_image])

        return result, code, msg
