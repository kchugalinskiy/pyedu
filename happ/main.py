from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from happ.core.config import settings
from happ.api.api import api_router

app = FastAPI(
    title=settings.PROJECT_NAME
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*']
)

app.include_router(api_router)
