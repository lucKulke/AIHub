from pydantic import BaseModel


class ImageData(BaseModel):
    description: str
    number_of_pictures: int
    size: str
