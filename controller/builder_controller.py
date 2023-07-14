from fastapi import APIRouter, Depends, UploadFile, Form
from pydantic import BaseModel

from model.builder_model import BuilderType

from service.builder_service import BuilderTypeService, BuilderValueService
from util.token_util import JWTBearer
from util.wrap_util import wrap_get_list_response, wrap_response

api = APIRouter()
builder_type_service = BuilderTypeService()
builder_value_service = BuilderValueService()


@api.get('/builder_type')
@wrap_get_list_response
def get_list_builder_type(page: int = 0, size: int = 100):
    result, count, code, msg = builder_type_service.get_list({}, page, size)
    return result,  count, code, msg


@api.post('/builder_type',  dependencies=[Depends(JWTBearer(check_admin=True))])
@wrap_response
def create_builder_type(builder_type: BuilderType):
    item = {key: value.title() for (key, value) in builder_type.dict().items()}
    result, code, msg = builder_type_service.create(item)
    return result, code, msg


@api.put('/builder_type/{builder_type_id}', dependencies=[Depends(JWTBearer(check_admin=True))])
@wrap_response
def update_builder_type(builder_type_id: str, builder_type: BuilderType):
    result, code, msg = builder_type_service.update(
        builder_type_id, builder_type.dict())
    return result, code, msg


@api.delete('/builder_type/{builder_type_id}', dependencies=[Depends(JWTBearer(check_admin=True))])
@wrap_response
def delete_builder_type(builder_type_id: str):
    result, code, msg = builder_type_service.delete(builder_type_id)
    return result, code, msg


# Builder Value ------------------------------------------------------------------------------------------

@api.get('/builder_value')
@wrap_get_list_response
def get_list_builder_value(builder_type_id: str, page: int = 0, size: int = 100):
    _filter = {'builder_type_id': builder_type_id}
    result, count, code, msg = builder_value_service.get_list(
        _filter, page, size, deep=True)
    return result, count, code, msg


@api.post('/builder_value', dependencies=[Depends(JWTBearer(check_admin=True))])
@wrap_response
def create_builder_value(image: UploadFile = Form(...), builder_type_id: str = Form(...), name: str = Form(...)):
    create_item = {'builder_type_id': builder_type_id,
                   'name': name.title(), 'image': image}
    result, code, msg = builder_value_service.create(create_item)
    return result, code, msg


@api.put('/builder_value/{builder_value_id}', dependencies=[Depends(JWTBearer(check_admin=True))])
@wrap_response
def update_builder_value(builder_value_id: str, image: UploadFile = Form(...), builder_type_id: str = Form(...), name: str = Form(...)):
    update_item = {'builder_type_id': builder_type_id,
                   'name': name.title(), 'image': image}
    result, code, msg = builder_value_service.update(
        builder_value_id, update_item)
    return result, code, msg


@api.delete('/builder_value/{builder_value_id}', dependencies=[Depends(JWTBearer(check_admin=True))])
@wrap_response
def delete_builder_value(builder_value_id: str):
    result, code, msg = builder_value_service.delete(builder_value_id)
    return result, code, msg
