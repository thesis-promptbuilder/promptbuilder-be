from fastapi import APIRouter, Depends, File, Form, UploadFile
from pydantic import BaseModel

from service.image_service import ImageService
from util.token_util import JWTBearer
from util import pinecone
from util.const_util import PINECONE_NAMESPACE_USER
from util.wrap_util import wrap_get_list_response, wrap_response
from util import sqs

api = APIRouter()
image_service = ImageService()

MAX_IMAGE = 1


@api.get('/image')
@wrap_get_list_response
def get_list_image(user_id: str = None, user_sender_id: str = None, page: int = 0, size: int = 20):
    _filter = {}
    if user_id != None:
        _filter['user_id'] = user_id
    result, count, code, msg = image_service.get_list(_filter, page, size, deep=False)
    result = [image_service.get_extra_info({**item, 'user_sender_id': user_sender_id}) for item in result]
    return result, count, code, msg


@api.delete('/image/{image_id}', dependencies=[Depends(JWTBearer())])
@wrap_response
def delete_image(image_id: str):
    result, code, msg = image_service.delete(image_id)
    if code == 0:
        sqs.send_message({
            'action': 'delete',
            'id': image_id
        })
    return result, code, msg


@api.post('/image', dependencies=[Depends(JWTBearer())])
@wrap_response
def create_image(user_id: str = Form(...),
                 prompt_id: str = Form(...),
                 image: UploadFile = File(...)):
    result, code, msg = image_service.create({
        'user_id': user_id, 'prompt_id': prompt_id, 'image': image
    })
    return result, code, msg


@api.get('/image/{image_id}')
@wrap_response
def get_image(image_id: str):
    result, code, msg = image_service.get(image_id)
    return result, code, msg


@api.get('/image/search/semantic-search')
@wrap_response
def search_semantic(query: str, user_sender_id: str = None):
    user_prompt = pinecone.query(query=query, namespace=PINECONE_NAMESPACE_USER)
    user_prompt = [{**item, **item['metadata']} for item in user_prompt]

    result = [image_service.get_extra_info({**item, 'user_sender_id': user_sender_id}) for item in user_prompt]

    return result, 0, 'success'
