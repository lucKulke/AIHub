from fastapi import FastAPI, routing
from db import database_connection
from db import models
from routers import language_processing, text_to_voice, voice_to_text, image_generation
from security import security_routes, handler
import re

app = FastAPI()


engine = database_connection.engine

models.Base.metadata.create_all(bind=engine)


@app.on_event("startup")
async def startup_event():
    all_available_paths = []
    for route in app.routes:
        if isinstance(route, routing.APIRoute):
            match = re.search(r"/([^/]+)/?$", route.path)
            if match:
                last_word = match.group(1)
                all_available_paths.append(last_word)

    handler.fake_users_db["lucaskulke"]["scopes"] = all_available_paths
    print(all_available_paths, flush=True)


app.include_router(security_routes.router)
app.include_router(language_processing.router)
app.include_router(text_to_voice.router)
app.include_router(voice_to_text.router)
app.include_router(image_generation.router)
