import boto3
from botocore.exceptions import ClientError

from util.logger_util import logger
from util.const_util import AWS_S3_PREFIX, AWS_REGION_NAME, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY


class S3:
    def __init__(self, region_name=AWS_REGION_NAME, bucket_name='raw-data'):
        self.region_name = region_name
        self.bucket_name = self.norm_bucket_name(bucket_name)
        self.s3_client = boto3.client('s3',
                                      aws_access_key_id=AWS_ACCESS_KEY_ID,
                                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                                      region_name=region_name)
        
        self.s3_resource = boto3.resource('s3',
                            aws_access_key_id=AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                            region_name=self.region_name)
        
        # create bucket if not exist
        if not self.check_exist_bucket():
            self.create_bucket()

    def norm_bucket_name(self, bucket_name):
        if bucket_name is None:
            return self.bucket_name
        return f'{AWS_S3_PREFIX}-{bucket_name}'

    def check_exist_bucket(self):
        return self.s3_resource.Bucket(self.bucket_name) in self.s3_resource.buckets.all()

    def create_bucket(self):
        try:
            if self.region_name is None:
                return False
            else:
                location = {'LocationConstraint': self.region_name}
                self.s3_client.create_bucket(Bucket=self.bucket_name,
                                             CreateBucketConfiguration=location)
        except ClientError as e:
            logger.error(e)

    def put_object(self, object_data, object_name):
        try:
            self.s3_client.put_object(Body=object_data, Bucket=self.bucket_name, Key=str(object_name))
            return True
        except ClientError as e:
            logger.error(e)
            return False

    def upload_file(self, file_name, object_name):
        try:
            self.s3_client.upload_file(file_name, self.bucket_name, object_name)
            return True
        except ClientError as e:
            logger.error(e)
            return False

    def get_list_objects(self):
        bucket = self.s3_resource.Bucket(self.bucket_name)
        return bucket.objects.all()