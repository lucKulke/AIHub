from pydantic import BaseModel, Field
from typing import Dict


class Sections(BaseModel):
    role: str
    content: str


class Instance(BaseModel):
    system_message: str
    sections: list[Sections]


class ChatGPTSchema(BaseModel):
    instances: Dict[str, Instance]
    model: str = Field(default="gpt-3.5-turbo", description="chat-gpt model")
    token: int = Field(default=100, description="max token")
