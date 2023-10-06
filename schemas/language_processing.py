from pydantic import BaseModel


class ChatGPTSchema(BaseModel):
    instances: dict
    model: str
    token: int
