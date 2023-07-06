import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')

# mongo
MONGO_URL = os.getenv('MONGO_URL')

# pinecone
MODEL_NAME = os.getenv('MODEL_NAME')
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_ENV = os.getenv('PINECONE_ENV')
PINECONE_INDEX = os.getenv('PINECONE_INDEX')
PINECONE_NAMESPACE_USER = os.getenv('PINECONE_NAMESPACE_USER')

# openai
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# jwt
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')

# aws
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION_NAME = os.getenv('AWS_REGION_NAME')
AWS_CDN = os.getenv('AWS_CDN')
AWS_S3_PREFIX = os.getenv('AWS_S3_PREFIX')
AWS_SQS_GENERATE = os.getenv('AWS_SQS_GENERATE')

# mailtrap
MAILTRAP_KEY = os.getenv('MAILTRAP_KEY')

# discord
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
