from fastapi import FastAPI
from . import routes, models
from .database import engine

models.Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(routes.router)
