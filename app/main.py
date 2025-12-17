from fastapi import FastAPI
from . import routes, models
from .database import engine

models.Base.metadata.create_all(engine)

app = FastAPI(
    title="API de Sistema Financeiro",
    summary="Crie contas e faça transações",
    description="API com dois endpoints, podendo criar, "
    "acessar informações e requisitar transferência.",
    version="0.4",
    openapi_tags=routes.tags_metadata,
    contact={
        "name": "Yuri F. Pereira",
    },
    license_info={"name": "MIT"},
)

app.include_router(routes.router)
