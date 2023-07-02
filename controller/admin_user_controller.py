from fastapi import APIRouter, Depends, File, Form, UploadFile
from pydantic import BaseModel

from model.user_model import User, UserUpdate
from service.user_service import UserService
from util.token_util import JWTBearer
from util.wrap_util import wrap_get_list_response, wrap_response

api = APIRouter()
user_service = UserService()

# admin


@api.get('/user', dependencies=[Depends(JWTBearer(check_admin=True))])
@wrap_get_list_response
def get_list_user(page: int = 0, size: int = 100):
    result, count, code, msg = user_service.get_list({}, page, size)
    return result, count, code, msg


@api.get('/user/{user_id}', dependencies=[Depends(JWTBearer(check_admin=True))])
@wrap_response
def get_user(user_id: str, deep: bool = False):
    user, code, msg = user_service.get(user_id, deep)
    return user, code, msg


@api.put('/user/{user_id}', dependencies=[Depends(JWTBearer(check_admin=True))])
@wrap_response
def update_user(user_id: str, user: UserUpdate):
    result, code, msg = user_service.update(user_id, user.dict())
    return result, code, msg


@api.post('/user', dependencies=[Depends(JWTBearer(check_admin=True))])
@wrap_response
def create_user(user: User):
    result, code, msg = user_service.create(data=user.dict())
    return result, code, msg


@api.delete('/user/{user_id}', dependencies=[Depends(JWTBearer(check_admin=True))])
@wrap_response
def delete_user(user_id: str):
    result, code, msg = user_service.delete(user_id)
    return result, code, msg
