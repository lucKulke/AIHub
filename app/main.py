from fastapi import FastAPI, routing
from src.db.database_connection import engine, SessionLocal
from src.db import models, crud
from src.routers import (
    language_processing_routes,
    text_to_voice_routes,
    voice_to_text_routes,
    image_generation_routes,
)
from src.security import security_routes, security_schemas

import os
import re


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
app.include_router(language_processing_routes.router)
app.include_router(text_to_voice_routes.router)
app.include_router(voice_to_text_routes.router)
app.include_router(image_generation_routes.router)
