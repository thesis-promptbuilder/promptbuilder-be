import io
import requests
from PIL import Image
import uuid


def compress_image(image_src):
    try:
        res = requests.get(image_src)
        image = Image.open(io.BytesIO(res.content))
        file_name = image_src.split('/')[-1]

        image.save(file_name,
                   "JPEG",
                   optimize=True,
                   quality=10)
    except:
        return None

    return file_name


def compress_image(image_src):
    try:
        res = requests.get(image_src)
        image = Image.open(io.BytesIO(res.content))

        endfix = image_src.split('.')[-1]
        filename = f'{str(uuid.uuid1())}.${endfix}'

        image.save(filename,
                   "JPEG",
                   optimize=True,
                   quality=10)
    except:
        return None

    return filename
