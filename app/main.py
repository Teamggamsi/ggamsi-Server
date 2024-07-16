from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.main import api_router

app = FastAPI(
    title="못난이",
)

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router, prefix="/api")