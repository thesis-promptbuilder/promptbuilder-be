import re

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from service.prompt_service import PromptService
from util.token_util import JWTBearer
from util.wrap_util import wrap_get_list_response, wrap_response
from util import pinecone, sqs_generate_image
from util.const_util import PINECONE_NAMESPACE_USER

api = APIRouter()
prompt_service = PromptService()


class Prompt(BaseModel):
    user_id: str
    prompt: str
    negative_prompt: str = ''


@api.get('/prompt')
@wrap_get_list_response
def get_list_prompt(search: str = '', page: int = 0, size: int = 10):
    _filter = {'prompt': re.compile(search, re.IGNORECASE)}
    result, count, code, msg = prompt_service.get_list(_filter, page, size)
    return result, count, code, msg


@api.get('/prompt/user/{user_id}')
@wrap_get_list_response
def get_list_prompt_by_user(user_id: str, search: str = '', page: int = 0, size: int = 10):
    _filter = {'prompt': re.compile(search, re.IGNORECASE), 'user_id': user_id}
    result, count, code, msg = prompt_service.get_list(_filter, page, size)
    return result, count, code, msg


@api.get('/prompt/{prompt_id}')
@wrap_response
def get_prompt(prompt_id: str):
    result, code, msg = prompt_service.get(prompt_id, {}, deep=True)
    return result, code, msg


@api.delete('/prompt/{prompt_id}', dependencies=[Depends(JWTBearer())])
@wrap_response
def delete_prompt(prompt_id: str):
    result, code, msg = prompt_service.delete(prompt_id)
    return result, code, msg


@api.post('/prompt', dependencies=[Depends(JWTBearer())])
@wrap_response
def create_prompt(prompt: Prompt, generate_image: str = False):
    result, code, msg = prompt_service.create(prompt.dict())
    if generate_image:
        sqs_generate_image.send_message({
            'action': 'generate',
            **prompt.dict(),
            'prompt_id': result['id']
        })
    return result, code, msg


@api.get('/prompt/search/semantic-search')
@wrap_response
def search_semantic(query: str):
    crawl_prompt = pinecone.query(query)
    user_prompt = pinecone.query(query=query, namespace=PINECONE_NAMESPACE_USER)

    result = [item for item in crawl_prompt + user_prompt if item.get('score', 0) > 0.5]

    return result, 0, 'success'
