from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from controller.admin_user_controller import api as admin_user_controller
from controller.builder_controller import api as builder_controller
from controller.image_controller import api as image_controller
from controller.prompt_controller import api as prompt_controller
from controller.upvote_controller import api as upvote_controller
from controller.user_controller import api as user_controller
from controller.generate_controller import api as generate_controller

blueprint = FastAPI(title='thesis-be-service', version='1.0',
                    swagger_ui_parameters={"docExpansion": "none"})

blueprint.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@blueprint.get('/')
def health_check():
    return {'message': 'Hello World!'}


blueprint.include_router(user_controller, prefix="/api", tags=["User"])
blueprint.include_router(upvote_controller, prefix="/api", tags=["Upvote"])
blueprint.include_router(prompt_controller, prefix="/api", tags=["Prompt"])
blueprint.include_router(image_controller, prefix="/api", tags=["Image"])
blueprint.include_router(builder_controller, prefix="/api", tags=["Builder"])
blueprint.include_router(generate_controller, prefix="/api", tags=["Generate"])
blueprint.include_router(admin_user_controller, prefix="/api/admin", tags=["Admin User"])
