import pymongo
from service.image_service import ImageService
from util.image_util import compress_image
from util.const_util import MONGO_DB_NAME
from PIL import Image as PILImage
import os
import json


image_service = ImageService()

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient[MONGO_DB_NAME]
mycol = mydb['discordMessage']


def parse_data(item):
    result = mycol.find_one({})
    item = result

    file_name = compress_image(item['image_src'])
    if file_name is None:
        return None

    parse_data = {
        'user_id': '64b0d72bea2c878aaa6fa5a6',
        'prompt': item['prompt'],
        'image': {
            'file': PILImage.open(file_name),
            'filename': file_name
        }
    }

    return parse_data


def parse_to_handle_duplicate():
    for page in range(0, 1000):
        limit = 5000
        skip = limit * page
        result = mycol.find(
            filter={}, limit=limit, skip=skip
        )

        list_prompt = []
        list_image_src = []

        for item in result:
            list_prompt.append(item['prompt'])
            list_image_src.append(item['image_src'])

        if len(list_prompt) == 0:
            break

        data = json.dumps({
            'prompt': list_prompt,
            'image_src': list_image_src
        })

        if not os.path.exists('crawl/parse_data'):
            os.mkdir('crawl/parse_data')

        with open(f"crawl/parse_data/{page}.json", "w") as outfile:
            outfile.write(data)


if __name__ == '__main__':
    parse_to_handle_duplicate()
