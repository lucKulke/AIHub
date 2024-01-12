from pydantic import BaseModel


class TextToVoice(BaseModel):
    text: str
    language: str
