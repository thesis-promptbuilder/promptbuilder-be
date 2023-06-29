from util.pinecone import Pinecone
from util.sqs import SQS
from util.s3_util import S3
from util.const_util import AWS_SQS_NAME, AWS_SQS_GENERATE

sqs = SQS(queue_name=AWS_SQS_NAME)
sqs_generate_image = SQS(queue_name=AWS_SQS_GENERATE)

s3_image = S3(bucket_name='image')

pinecone = Pinecone()
