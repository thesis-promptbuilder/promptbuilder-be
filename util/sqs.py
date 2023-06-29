import boto3
import json
from util.logger_util import logger
from util.const_util import AWS_REGION_NAME, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY


class SQS:
    def __init__(self, region_name=AWS_REGION_NAME, queue_name='thesis', fifo='false'):
        self.region_name = region_name
        self.queue_name = f'{queue_name}.fifo' if fifo == 'true' else queue_name
        self.fifo = fifo
        self.sqs_client = boto3.client("sqs",
                                       aws_access_key_id=AWS_ACCESS_KEY_ID,
                                       aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                                       region_name=self.region_name)
        logger.info(f'SQS: {self.region_name} | {self.queue_name}')

    def create_queue(self):
        response = None
        attributes = {'VisibilityTimeout': '30'}
        if self.fifo == 'true':
            attributes['FifoQueue'] = 'true'
        try:
            response = self.sqs_client.create_queue(
                QueueName=self.queue_name,
                Attributes=attributes
            )
        except Exception as e:
            logger.error(e)
            return response

        return response

    def get_queue_url(self):
        response = None
        try:
            response = self.sqs_client.get_queue_url(
                QueueName=self.queue_name,
            )
        except Exception as e:
            logger.error(e)
            return response

        return response["QueueUrl"]

    def send_message(self, message):
        response = None
        logger.info(f'Send message {message} to {self.queue_name}')
        try:
            response = self.sqs_client.send_message(
                QueueUrl=self.get_queue_url(),
                MessageBody=json.dumps(message),
            )
        except Exception as e:
            logger.error(e)
            return response

        return response

    def receive_message(self):
        logger.info('SQS is receiving message')
        messages = []
        try:
            queue_url = self.get_queue_url()
            response = self.sqs_client.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=10,
                WaitTimeSeconds=10,
            )
            messages = response.get('Messages', [])
            logger.info(f'There are {len(messages)} messages')
        except Exception as e:
            logger.error(e)
            return messages

        return messages

    def delete_message(self, messages):
        logger.info(f'SQS is deleting {len(messages)} message ')
        try:
            if len(messages) > 0:
                message_ids = [{
                    'Id': message['MessageId'],
                    'ReceiptHandle': message['ReceiptHandle']
                } for message in messages]
                self.sqs_client.delete_message_batch(QueueUrl=self.get_queue_url(),
                                                     Entries=message_ids)
                logger.info('SQS delete messages success')
        except Exception as e:
            logger.error(e)
