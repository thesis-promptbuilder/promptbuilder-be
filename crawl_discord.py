from util.const_util import DISCORD_TOKEN
from util.s3_util import S3
from util.image_util import compress_image
import requests
import json
import uuid
from util.time_util import get_time_string

s3_discord = S3(bucket_name='discord')


def crawl_message(url):
    response = requests.get(url, headers={'Authorization': DISCORD_TOKEN})

    if response.status_code == 200:
        return response.json()

    return None


def crawl_channel(channel_id, before=None):
    base_url = f'https://discord.com/api/v9/channels/{channel_id}/messages?limit=50'
    if before is not None:
        base_url += f'&before={before}'
    result = crawl_message(base_url)

    if result is None:
        return None

    s3_discord.put_object(json.dumps(result), f'{get_time_string()}/{str(uuid.uuid1())}')
    _id_before = None

    for sen in result:
        attachments = sen.get('attachments', [])
        prompt = sen.get('content', '')
        _id = sen.get('id', None)

        if _id is None or len(attachments) == 0:
            continue

        _id_before = _id
        # image_file = compress_image(attachments[0]['url'])

    return _id_before


if __name__ == '__main__':
    channel_id = '1008571159043903509'
    while True:
        _id_before = crawl_channel(channel_id)
