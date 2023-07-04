from functools import wraps
from util.token_util import decode_token
from fastapi import Request


def wrap_response(func):
    @wraps(func)
    def inner(*args, **kwargs):
        items, code, msg = func(*args, **kwargs)
        return {'result': items, 'code': code, 'msg': msg}

    return inner


def wrap_get_list_response(func):
    @wraps(func)
    def inner(*args, **kwargs):
        items, count, code, msg = func(*args, **kwargs)
        return {'result': items, 'count': count, 'code': code, 'msg': msg}

    return inner


def wrap_authorization(func):
    @wraps(func)
    def inner(*args, req: Request, **kwargs):
        token = req.headers['authorization'].split()[-1]
        user = decode_token(token)
        user_id = kwargs.get('user_id', '')
        user_id_in_token = user.get('id', None)
        user_role = user.get('role', 'user')

        if user_id != user_id_in_token and user_id and user_id_in_token:
            # not valid token and not is a admin
            if user_role != 'admin':
                return None, -1, 'invalid user'

        result, code, msg = func(*args, req, **kwargs)
        return result, code, msg

    return inner
