from util.const_util import DISCORD_TOKEN
from util.s3_util import S3
from util.image_util import compress_image
import requests
import json
import os
import uuid
from util.time_util import get_time_string, now
from service.image_service import ImageService


s3_discord = S3(bucket_name='discord')
image_service = ImageService()

user_id = '64a7d1ca419d379db65d71eb'


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

    _id_before = export_to_json(result)
    s3_discord.put_object(json.dumps(result), f'{get_time_string()}/{str(uuid.uuid1())}')

    return _id_before


def export_to_json(result):
    print('start to export')
    # json_file_name = f'{get_time_string()}-{str(uuid.uuid1())}'
    data = {'result': []}
    for index, sen in enumerate(result):
        print('--- index', index)
        attachments = sen.get('attachments', [])
        prompt = sen.get('content', '')
        author = sen.get('author', None)
        channel_id = sen.get('channel_id', '')
        message_id = sen.get('id', None)

        if message_id is None \
                or len(attachments) == 0 \
                or author.get('username', '') != 'Midjourney Bot' \
                or not prompt \
                or 'Image #' in prompt:
            continue

        _id_before = message_id

        clean_prompt = prompt.split('**')[1]
        image_file = compress_image(attachments[0]['url'])

        data['result'].append({
            'user_id': user_id,
            'message_id': message_id,
            'channel_id': channel_id,
            'prompt': clean_prompt,
            'image': {
                'filename': image_file
            }
        })

    # print(len(data['result']) / len(result), '--', len(data['result']))
    # write_to_json(data, json_file_name)
    write_to_mongo(data['result'])

    return _id_before


def write_to_json(data, filename):
    json_object = json.dumps(data)

    if not os.path.exists('crawl/result'):
        os.mkdir('crawl/result')
    # with open(f"crawl/result/{filename}.json", "w") as outfile:
    #     outfile.write(json_object)


def write_to_mongo(data):
    _, code, msg = image_service.create_many(data)
    print(code, msg)


if __name__ == '__main__':
    channel_id = '1008571102328541215'

    _id_before = crawl_channel(channel_id)

    while True:
        _id_before = crawl_channel(channel_id, before=_id_before)
        print('Done', _id_before)
        import time
        time.sleep(3)
