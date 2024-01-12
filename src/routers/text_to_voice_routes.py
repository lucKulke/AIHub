from fastapi import APIRouter, Response, HTTPException, Security
from fastapi.responses import JSONResponse
import requests
import os
from ..utilitys import azure
from ..schemas.text_to_voice_schemas import TextToVoice
from ..ai_services.text_to_voice_services import AzureVoice
from typing import Annotated
from ..security.handler import get_current_active_user
from ..security.security_schemas import User

router = APIRouter(prefix="/text_to_voice", tags=["Text to voice"])

subscription_key = os.getenv("AZURE_VOICE_SUBSCRIPTION_KEY")
azure_token_url = os.getenv("AZURE_TOKEN_URL")
ctms_base_url = os.getenv("CTMS")
azure_voice = AzureVoice(
    subscription_key=subscription_key,
    azure_token_url=azure_token_url,
    ctms_url=f"{ctms_base_url}/get_azure_token",
)


@router.post("/azure")
def generate_azure_voice(
    current_user: Annotated[User, Security(get_current_active_user, scopes=["azure"])],
    request: TextToVoice,
):
    if not azure_voice.is_language_available(request.language):
        raise HTTPException(
            status_code=404,
            detail=f"'{request.language}' not available. Go to /voice_to_text/azure/list for all available languages",
        )

    response = azure_voice.generate_voice(text=request.text, language=request.language)

    if response.status_code != 200:
        HTTPException(status_code=response.status_code, detail=response.text)

    audio_data = response.content

    headers = {
        "Content-Disposition": "attachment; filename=generated_audio.wav",
        "Content-Type": "audio/wav",
    }

    return Response(content=audio_data, headers=headers)


@router.get("/azure/available_voices")
def azure_voices():
    return azure_voice.list_of_available_languages()


@router.get("/azure/speakers")
def azure_speakers():
    content = azure_voice.list_of_azure_voices()

    return Response(
        content=content, headers={"Content-Type": "application/json; charset=utf-8"}
    )
