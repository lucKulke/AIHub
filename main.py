from fastapi import FastAPI
from db import database_connection
from db import models
from routers import language_processing, text_to_voice, voice_to_text, image_generation
from security import security_routes

app = FastAPI()


engine = database_connection.engine

models.Base.metadata.create_all(bind=engine)


app.include_router(security_routes.router)
app.include_router(language_processing.router)
app.include_router(text_to_voice.router)
app.include_router(voice_to_text.router)
app.include_router(image_generation.router)
