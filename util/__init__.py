import pymongo

from util.pinecone import Pinecone
from util.sqs import SQS
from util.s3_util import S3
from util.const_util import AWS_SQS_GENERATE, PINECONE_NAMESPACE_USER, MONGO_URL

# aws
sqs_generate_image = SQS(queue_name=AWS_SQS_GENERATE)
s3_image = S3(bucket_name='image')

# pinecone
pinecone = Pinecone()
pinecone_user_prompt = Pinecone(namespace=PINECONE_NAMESPACE_USER)

# mongo
mongo_client = pymongo.MongoClient(MONGO_URL)
