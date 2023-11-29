from fastapi import APIRouter, Response, HTTPException, Security
from fastapi.responses import JSONResponse
import requests
import os
from utilitys import azure
from schemas.text_to_voice import TextToVoice
from ai_services.text_to_voice import AzureVoice

from typing import Annotated
from security.handler import get_current_active_user
from security.security_schemas import User

subscription_key = os.getenv("AZURE_VOICE_SUBSCRIPTION_KEY")
router = APIRouter(prefix="/text_to_voice", tags=["Text to voice"])


@router.post("/azure")
def azure_voice(
    current_user: Annotated[User, Security(get_current_active_user, scopes=["azure"])],
    request: TextToVoice,
):
    azure_voice = AzureVoice()

    if not azure_voice.is_language_available(request.language):
        raise HTTPException(
            status_code=404,
            detail=f"'{request.language}' not available. Go to /voice_to_text/azure/list for all available languages",
        )

    access_token = azure.get_access_token(subscription_key=subscription_key)

    azure_voice.set_access_token(access_token)

    response = azure_voice.generate_voice(text=request.text, language=request.language)

    if response.status_code != 200:
        HTTPException(status_code=response.status_code, detail=response.text)

    audio_data = response.content  # Replace with your audio generation logic

    # Set the content type header to indicate that it's an audio file (e.g., WAV)
    headers = {
        "Content-Disposition": "attachment; filename=generated_audio.wav",
        "Content-Type": "audio/wav",
    }
    # Return the audio file as a response
    return Response(content=audio_data, headers=headers)
    # Check the response status code and content


@router.get("/azure/available_voices")
def azure_voices():
    return AzureVoice().list_of_available_languages()


@router.get("/azure/speakers")
def azure_speakers():
    content = AzureVoice().list_of_azure_voices(subscription_key)
    return Response(
        content=content, headers={"Content-Type": "application/json; charset=utf-8"}
    )
    return AzureVoice().list_of_azure_voices(subscription_key)
