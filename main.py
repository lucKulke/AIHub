from fastapi import FastAPI, routing
from db.database_connection import engine, SessionLocal
from db import models
from routers import language_processing, text_to_voice, voice_to_text, image_generation
from security import security_routes, handler, security_schemas

from db import crud
import re, os


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def find_all_available_paths():
    all_available_paths = []
    for route in app.routes:
        if isinstance(route, routing.APIRoute):
            match = re.search(r"/([^/]+)/?$", route.path)
            if match:
                last_word = match.group(1)
                all_available_paths.append(last_word)
    return all_available_paths


@app.on_event("startup")
async def startup_event():
    db = SessionLocal()
    try:
        all_scopes = find_all_available_paths()
        admin = security_schemas.NewUser(
            username=os.getenv("AIHUB_ADMIN_USERNAME"),
            password=os.getenv("AIHUB_ADMIN_PASSWORD"),
            disabled=False,
            scopes=all_scopes,
        )
        response = crud.create_admin(db=db, new_user=admin)
        db.commit()
    finally:
        db.close()
    print(response, flush=True)


app.include_router(security_routes.router)
app.include_router(language_processing.router)
app.include_router(text_to_voice.router)
app.include_router(voice_to_text.router)
app.include_router(image_generation.router)
