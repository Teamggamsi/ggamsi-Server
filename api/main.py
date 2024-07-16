from fastapi import APIRouter

from api.routes import login,rank

api_router = APIRouter()
api_router.include_router(login.router, tags=["Auth"])
api_router.include_router(rank.router, tags=["Rank"])
