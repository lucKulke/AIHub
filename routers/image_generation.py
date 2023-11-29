from fastapi import APIRouter, Security
from typing import Union, Annotated

import os
from ai_services.image_generation import Dalle
from schemas.image_generation import ImageData

from security.handler import get_current_active_user

from security.security_schemas import User

router = APIRouter(prefix="/image_generation", tags=["Image generation"])


@router.post("/dalle")
async def generate_dalle_response(
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["create_user"])
    ],
    image_data: ImageData,
):
    open_ai_key = os.getenv("OPEN_AI_KEY")
    response = Dalle(open_ai_key).request(
        image_data.description, image_data.number_of_pictures, image_data.size
    )
    return {"url": response}
