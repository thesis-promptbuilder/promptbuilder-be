import re

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel

from service.prompt_service import PromptService
from util.token_util import JWTBearer
from util.wrap_util import wrap_authorization, wrap_get_list_response, wrap_response
from util import pinecone, sqs_generate_image
from util.const_util import PINECONE_NAMESPACE_USER

api = APIRouter()
prompt_service = PromptService()


class Prompt(BaseModel):
    user_id: str
    prompt: str
    negative_prompt: str = ''


@api.post('/prompt', dependencies=[Depends(JWTBearer())])
@wrap_response
@wrap_authorization
def create_prompt(req: Request, user_id: str, prompt: Prompt, generate_image: str = False):
    if generate_image:
        sqs_generate_image.send_message({
            **prompt.dict(),
        })
    return prompt.dict(), 0, 'success'


@api.get('/prompt/search/semantic-search')
@wrap_response
def search_semantic(query: str):
    crawl_prompt = pinecone.query(query)
    user_prompt = pinecone.query(query=query, namespace=PINECONE_NAMESPACE_USER)

    result = [item for item in crawl_prompt + user_prompt if item.get('score', 0) > 0.5]

    return result, 0, 'success'
