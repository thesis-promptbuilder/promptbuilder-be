import json
import pymongo

from util.s3_util import S3

s3_discord = S3(bucket_name='discord')

list_objects = s3_discord.get_list_objects()


def init_mongo():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["thesisDB"]
    collection = db["discordMessage"]

    collection.create_index([('message_id', pymongo.ASCENDING),
                            ('channel_id', pymongo.ASCENDING)],
                            name='messageId_channelId', unique=True)

    return collection


def clean_message(msg):
    message_id = msg.get('id', None)
    channel_id = msg.get('channel_id', '')
    attachments = msg.get('attachments', [])
    prompt = msg.get('content', '')
    author = msg.get('author', None)
    username = author.get('username', '')

    if message_id is None \
        or len(attachments) == 0 \
            or username != 'Midjourney Bot' \
        or not prompt \
    or 'Image #' in prompt:
        return None

    if len(prompt.split('**')) < 2:
        return None

    clean_prompt = prompt.split('**')[1]
    image_src = attachments[0]['url']

    return {
        'message_id': message_id,
        'channel_id': channel_id,
        'prompt': clean_prompt,
        'image_src': image_src
    }


def clean_list_messages(list_messages):
    list_valid_messages = []
    for msg in list_messages:
        clean_msg = clean_message(msg)
        if clean_msg is not None:
            list_valid_messages.append(clean_msg)

    return list_valid_messages


def import_to_mongo(collection, list_valid_messages):
    try:
        res = collection.insert_many(list_valid_messages)
        return res.inserted_ids
    except:
        return None


if __name__ == '__main__':
    collection = init_mongo()

    count = 0
    for obj in list_objects:
        body = obj.get()['Body'].read()
        list_messages = json.loads(body)
        list_valid_messages = clean_list_messages(list_messages)

        # import to mongo
        import_to_mongo(collection, list_valid_messages)
        count += 1
        if count % 10000 == 0:
            print('----- done ----', count)
