import os
from fastapi import APIRouter, Depends, File, Form, Request, UploadFile
from pydantic import BaseModel
from util import pinecone_user_prompt

from service.image_service import ImageService
from util.token_util import JWTBearer
from util.wrap_util import wrap_authorization, wrap_get_list_response, wrap_response

api = APIRouter()
image_service = ImageService()

MAX_IMAGE = 1


@api.get('/image')
@wrap_get_list_response
def get_list_image(query: str = None, user_id: str = None, page: int = 0, size: int = 20):
    _filter = {}
    if user_id != None:
        _filter['user_id'] = user_id
    if query != None:
        _filter['prompt'] = {'$regex': f'^{query}$', '$options': 'i'}
    result, count, code, msg = image_service.get_list(
        _filter, page, size, deep=False)
    result = [image_service.get_extra_info({**item}) for item in result]
    return result, count, code, msg


@api.delete('/image/{image_id}', dependencies=[Depends(JWTBearer())])
@wrap_response
@wrap_authorization
def delete_image(req: Request,  image_id: str, user_id: str):
    _id, code, msg = image_service.delete(image_id)
    return _id, code, msg


@api.post('/image', dependencies=[Depends(JWTBearer())])
@wrap_response
@wrap_authorization
def create_image(
        req: Request,
        user_id: str = Form(...),
        prompt: str = Form(...),
        image: UploadFile = File(...)):
    result, code, msg = image_service.create({
        'user_id': user_id,
        'prompt': prompt,
        'image': image
    })
    return result, code, msg


@api.get('/image/{image_id}')
@wrap_response
def get_image(image_id: str):
    result, code, msg = image_service.get(image_id)
    return result, code, msg


@api.get('/image/search/semantic-search')
@wrap_response
def search_semantic(query: str):
    user_prompt = pinecone_user_prompt.query(query=query, top_k=200)
    user_prompt = [{**item, **item['metadata']} for item in user_prompt]

    # only get result which has score > 0.5
    result = [image_service.get_extra_info({**item}) for item in user_prompt]

    return result, 0, 'success'


class ImageGenerate(BaseModel):
    user_id: str
    prompt: str
    image_src: str


@api.post('/upsert_after_generate')
@wrap_response
def upsert_after_generate(image: ImageGenerate):
    result, code, msg = image_service.upsert_after_generate(image.dict())
    return result, code, msg
