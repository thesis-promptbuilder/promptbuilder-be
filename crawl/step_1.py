from util.const_util import DISCORD_TOKEN
from util.s3_util import S3
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
    
    print(f'scrape done, channel_id: {channel_id}, message_before: {before}, len result: {len(result)}')
    s3_discord.put_object(json.dumps(result), f'{get_time_string()}/{channel_id}/{str(uuid.uuid1())}')
    _id_before = result[-1]['id']

    return _id_before


if __name__ == '__main__':

    # channel_id = '1008571102328541215' # newbie_127
    # channel_id = '1008571159043903509' # newbie_157
    channel_id = '1008571225309728878' # newbie_187

    _id_before = crawl_channel(channel_id)

    while True:
        _id_before = crawl_channel(channel_id, before=_id_before)
        if _id_before is None:
            break
        import time
        time.sleep(2)
