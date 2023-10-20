from fastapi import APIRouter
from typing import Union
from datetime import datetime
import asyncio
import os
from ai_services.image_generation import Dalle
from schemas.image_generation import ImageData


router = APIRouter(prefix="/image_generation", tags=["Image generation"])


@router.post("/dalle")
async def generate_chat_gpt_response(image_data: ImageData):
    open_ai_key = os.getenv("OPEN_AI_KEY")
    response = Dalle(open_ai_key).request(
        image_data.description, image_data.number_of_pictures, image_data.size
    )
    return {"url": response}
