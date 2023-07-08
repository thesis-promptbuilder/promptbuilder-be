import io
import requests
from PIL import Image
import uuid
import os


def compress_image(image_src):
    try:
        res = requests.get(image_src)
        image = Image.open(io.BytesIO(res.content))

        if not os.path.exists('image'):
            os.mkdir('image')

        endfix = image_src.split('.')[-1]
        file_name = f'image/{str(uuid.uuid1())}.{endfix}'

        image.save(file_name,
                   "JPEG",
                   optimize=True,
                   quality=10)
    except:
        return None

    return file_name
