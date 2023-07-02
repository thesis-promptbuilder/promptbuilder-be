from model.user_model import UserModel
from service.base_service import BaseService
from util.logger_util import logger
from util.error_util import Error


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

        if not (username and gmail and password):
            return None, -1, 'invalid data'

        result, code, msg = self.model.create({
            'username': username,
            'gmail': gmail,
            'password': password,
            'role': 'user',
            'is_ban': False,
            'is_activate': True
        })

        return result, code, msg
