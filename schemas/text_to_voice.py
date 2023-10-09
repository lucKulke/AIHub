from pydantic import BaseModel
from fastapi import UploadFile


class VoiceToText(BaseModel):
    text: str
