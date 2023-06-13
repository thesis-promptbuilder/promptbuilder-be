import threading

import bson
import pymongo

from model.base_mongodb import BaseMongoModel
from util.error_util import Error
from util.logger_util import logger


class Singleton(type):
    _lock = threading.Lock()
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super(
                        Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class BaseService(object, metaclass=Singleton):
    def __init__(self, model: BaseMongoModel):
        self.model = model

    def build_item(self, item):
        return item, 0, 'Item is validated'

    def create(self, data):
        try:
            item, code, msg = self.build_item(data)
            if item is None:
                return None, code, msg
            logger.debug(f'Build item: {msg}\n{item}')
            created_item, code, msg = self.model.create(item)
            return created_item, code, msg
        except Exception as e:
            logger.error(e, exc_info=True)
            return None, Error.ERROR_CODE_GOT_EXCEPTION, e

    def get_extra_info(self, item):
        return item

    def get(self, id, _filter={}, deep=False):
        try:
            item, code, msg = self.model.get(id, _filter=_filter)
            if not item:
                return None, Error.ERROR_CODE_GOT_NO_SUCH_ITEM, Error.ERROR_MESSAGE_GOT_NO_SUCH_ITEM
            if deep:
                item = self.get_extra_info(item)
            return item, code, msg
        except Exception as e:
            logger.error(e, exc_info=True)
            return None, Error.ERROR_CODE_GOT_EXCEPTION, e

    def get_list(self, _filter, page=0, size=10, order_by='update_time', order=-1, deep=False):
        try:

            items, code, msg = self.model.get_many(
                _filter=_filter, page=page, size=size, order_by=order_by, order=order)
            if deep:
                items = [self.get_extra_info(item) for item in items]

            return items, code, msg
        except Exception as e:
            logger.error(e, exc_info=True)
            return None, 0, Error.ERROR_CODE_GOT_EXCEPTION, e

    def build_update_item(self, update_item):
        return update_item, 0, 'Item is validated'

    def update(self, id, data):
        try:
            data.pop('create_time', None)
            data.pop('update_time', None)
            item, code, msg = self.build_update_item(data)
            if item is None:
                return None, code, msg
            item = {k: v for k, v in item.items() if v is not None}

            update_count, code, msg = self.model.update(id, item=item)
            if update_count:
                item, _, _ = self.get(id)
                return item, code, msg
            return None, -1, 'None of item was updated'
        except Exception as e:
            logger.error(e, exc_info=True)
            return None, Error.ERROR_CODE_GOT_EXCEPTION, e

    def delete(self, id):
        try:
            delete_count, code, msg = self.model.delete(id)
            if delete_count:
                return id, code, msg
            return None, -1, 'None of item was deleted'
        except Exception as e:
            logger.error(e, exc_info=True)
            return None, Error.ERROR_CODE_GOT_EXCEPTION, e