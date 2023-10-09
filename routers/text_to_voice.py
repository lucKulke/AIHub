from fastapi import APIRouter, Response, HTTPException
import requests
import os
import io
from pydub import AudioSegment
from utilitys import azure
from schemas.text_to_voice import VoiceToText

subscription_key = os.getenv("AWS_VOICE_SUBSCRIPTION_KEY")
router = APIRouter(prefix="/text_to_voice", tags=["Text to voice"])


@router.post("/microsoft")
def microsoft_voices(request: VoiceToText):
    access_token = azure.get_access_token(subscription_key=subscription_key)
    response = azure.text_to_voice(access_token=access_token, text=request.text)

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
