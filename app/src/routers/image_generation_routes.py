from fastapi import APIRouter, Security
from typing import Union, Annotated

import os
from ..ai_services.image_generation_services import Dalle
from ..schemas.image_generation_schemas import ImageData

from ..security.handler import get_current_active_user

from ..security.security_schemas import User

router = APIRouter(prefix="/image_generation", tags=["Image generation"])

dalle = Dalle(os.getenv("OPEN_AI_KEY"))


@router.post("/dalle")
async def generate_dalle_response(
    current_user: Annotated[User, Security(get_current_active_user, scopes=["dalle"])],
    image_data: ImageData,
):
    response = dalle.request(
        image_data.description, image_data.number_of_pictures, image_data.size
    )
    return {"url": response}
