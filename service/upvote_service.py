from model.upvote_model import UpvoteModel
from service.base_service import BaseService
from util.const_util import AWS_CDN
from util.logger_util import logger


class UpvoteService(BaseService):
    def __init__(self):
        super().__init__(UpvoteModel())

    def get_extra_info(self, item):
        from service.image_service import ImageService
        image, _, _ = ImageService().get(item['image_id'])
        if image is None:
            return item
        return {
            **item, 'prompt': image['prompt'], 'image_src': AWS_CDN + image['image_src']
        }
