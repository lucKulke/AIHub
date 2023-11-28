from fastapi import APIRouter, Depends, Security
from typing import Union, Annotated
from datetime import datetime

import asyncio
import os
from ai_services.language_processing import ChatGPT
from schemas.language_processing import ChatGPTSchema


from security.handler import get_current_active_user
from security.schemas import User

router = APIRouter(prefix="/language_processing", tags=["Language processing"])


@router.post("/chat_gpt")
async def generate_chat_gpt_response(
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["chat_gpt"])
    ],
    conversation: ChatGPTSchema,
):
    api_key = os.getenv("OPEN_AI_KEY")

    # crud.add_application(db, "Test app", 1)

    return await chat_gpt_response(
        ChatGPT(api_key),
        conversation.model,
        conversation.instances,
        conversation.token,
    )


async def chat_gpt_response(gpt_object, model, instances, token):
    tasks = []
    response = {}

    for instance, data in instances.items():
        sections = []

        for section in data.sections:
            sections.append({"role": section.role, "content": section.content})

        task = asyncio.create_task(
            gpt_object.request(instance, model, data.system_message, sections, token)
        )
        tasks.append(task)

    responses = await asyncio.gather(*tasks, return_exceptions=True)

    for i in responses:
        instance = list(i.keys())[0]
        response[instance] = i[instance]

    return response
