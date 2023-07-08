from typing import Literal

from fastapi import APIRouter, Depends, UploadFile, Form
from pydantic import BaseModel

from service.builder_service import BuilderTypeService, BuilderValueService
from util.token_util import JWTBearer
from util.wrap_util import wrap_get_list_response, wrap_response

api = APIRouter()
builder_type_service = BuilderTypeService()
builder_value_service = BuilderValueService()


class BuilderType(BaseModel):
    parent: str
    name: str


class BuilderValue(BaseModel):
    name: str


@api.get('/builder_type')
@wrap_get_list_response
def get_list_builder_type(page: int = 0, size: int = 100, parent: str = 'Style'):
    result, count, code, msg = BuilderTypeService().get_list({'parent': parent}, page, size)
    return result, count, code, msg


@api.post('/builder_type',  dependencies=[Depends(JWTBearer(check_admin=True))])
@wrap_response
def create_builder_type(builder_type: BuilderType):
    item = {key: value.title() for (key, value) in builder_type.dict().items()}
    result, code, msg = BuilderTypeService().create(item)
    return result, code, msg


@api.delete('/builder_type/{builder_type_id}', dependencies=[Depends(JWTBearer(check_admin=True))])
@wrap_response
def delete_builder_type(builder_type_id: str):
    result, code, msg = BuilderTypeService().delete(builder_type_id)
    return result, code, msg


# Builder Value ------------------------------------------------------------------------------------------

@api.get('/builder_value')
@wrap_get_list_response
def get_list_builder_value(builder_type: str = 'Layouts', page: int = 0, size: int = 100):
    _filter = {'parent': builder_type}
    result, count, code, msg = BuilderValueService().get_list(_filter, page, size, deep=True)
    return result, count, code, msg


@api.post('/builder_value', dependencies=[Depends(JWTBearer(check_admin=True))])
@wrap_response
def create_builder_value(image: UploadFile = Form(...), parent: str = Form(...), name: str = Form(...)):
    result, code, msg = BuilderValueService().create({'parent': parent.title(), 'name': name.title(), 'image': image})
    return result, code, msg


@api.put('/builder_value/{builder_value_id}', dependencies=[Depends(JWTBearer(check_admin=True))])
@wrap_response
def update_builder_value(builder_value_id: str, builder_value: BuilderValue):
    result, code, msg = BuilderValueService().update(builder_value_id, builder_value.dict())
    return result, code, msg


@api.delete('/builder_value/{builder_value_id}', dependencies=[Depends(JWTBearer(check_admin=True))])
@wrap_response
def delete_builder_value(builder_value_id: str):
    result, code, msg = BuilderValueService().delete(builder_value_id)
    return result, code, msg
