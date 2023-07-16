import os
import json
from service.image_service import ImageService
from util.image_util import compress_image
from PIL import Image as PILImage
from util.logger_util import logger

image_service = ImageService()

user_id = '64b0d72bea2c878aaa6fa5a6'


def import_to_db(file_path):
    data = json.load(open(file_path, 'r'))
    list_prompt = data['prompt']
    list_image_src = data['image_src']

    data = []
    for prompt, image_src in zip(list_prompt, list_image_src):
        try:
            file_name = compress_image(image_src)
            file_image = PILImage.open(file_name)
            data.append({
                'user_id': user_id,
                'prompt': prompt,
                'image': {
                    'file': file_image,
                    'filename': file_name
                }})

            if len(data) == 100:
                logger.info('done')
                image_service.create_many(data)
                data = []

        except Exception as e:
            logger.error(e)
            logger.error(f'{file_path}, {prompt}, {image_src}')
            continue

    if len(data) > 0:
        image_service.create_many(data)

    print('done', file_path)


if __name__ == '__main__':
    data_path = 'crawl/clean_data'
    for _file in os.listdir(data_path):
        import_to_db(f'{data_path}/{_file}')
