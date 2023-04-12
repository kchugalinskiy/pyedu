from fastapi import APIRouter

from happ.api.endpoints import hello

api_router = APIRouter()
api_router.include_router(hello.router)
