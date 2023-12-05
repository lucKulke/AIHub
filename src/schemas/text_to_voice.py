from pydantic import BaseModel
from typing import List


class TextToVoice(BaseModel):
    text: str
    language: str
