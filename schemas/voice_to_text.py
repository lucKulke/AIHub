from pydantic import BaseModel
from fastapi import UploadFile


class WhisperSchema(BaseModel):
    audiofile: UploadFile
    model: str
