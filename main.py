from fastapi import FastAPI, routing, Depends
from typing import Annotated
from db.database_connection import engine, SessionLocal, get_db
from db import models
from routers import language_processing, text_to_voice, voice_to_text, image_generation
from security import security_routes, handler


from db import crud
from sqlalchemy.orm import Session
import re, os


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    db = SessionLocal()
    try:
        all_paths = find_all_available_paths()
        string_of_all_paths = ",".join(all_paths)
        response = crud.create_admin(
            db=db,
            username=os.getenv("AIHUB_ADMIN_USERNAME"),
            password=os.getenv("AIHUB_ADMIN_PASSWORD"),
            scopes=string_of_all_paths,
        )
        db.commit()
    finally:
        db.close()
    print(response, flush=True)
    handler.fake_users_db["lucaskulke"]["scopes"] = all_paths


# @app.get("/test/")
# async def test(db: Session = Depends(get_db)):
#     all_paths = find_all_available_paths()
#     string_of_all_paths = ",".join(all_paths)
#     response = crud.create_admin(
#         db=db,
#         username=os.getenv("AIHUB_ADMIN_USERNAME"),
#         password=os.getenv("AIHUB_ADMIN_PASSWORD"),
#         scopes=string_of_all_paths,
#     )
#     db.commit()
#     print(response, flush=True)


# # finally:
# #     # db.close()
# #     pass


def find_all_available_paths():
    all_available_paths = []
    for route in app.routes:
        if isinstance(route, routing.APIRoute):
            match = re.search(r"/([^/]+)/?$", route.path)
            if match:
                last_word = match.group(1)
                all_available_paths.append(last_word)
    return all_available_paths


app.include_router(security_routes.router)
app.include_router(language_processing.router)
app.include_router(text_to_voice.router)
app.include_router(voice_to_text.router)
app.include_router(image_generation.router)
