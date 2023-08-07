from util.const_util import OPENAI_API_KEY
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI

llm = OpenAI(model_name='gpt-3.5-turbo',
             openai_api_key=OPENAI_API_KEY, temperature=0.5)

prompt = PromptTemplate.from_template(
    "you are an artist, a writer, a photographer. \
    I will give you some words, they are  {subjects}. \
    You have to combine those words in english and imagine to describe me a creative picture. \
    Your sentence should be simple, succinct, detail, max in 60 words, use collective nouns. \
    Your picture should has many subjects for detail. \
    You have to give me 10 creative sentences. \
    Show me result like an JSON with key is the order number of sentence and value is the sentence")
