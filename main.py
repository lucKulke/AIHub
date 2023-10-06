from fastapi import FastAPI
from db import database
from db import models
from routers import ai_service

app = FastAPI()


engine = database.engine

models.Base.metadata.create_all(bind=engine)


app.include_router(ai_service.router)
