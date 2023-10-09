from pydantic import BaseModel
from typing import List


class VoiceToText(BaseModel):
    text: str
    language: str
