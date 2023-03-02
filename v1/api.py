from fastapi import FastAPI, APIRouter, Request
from fastapi.middleware.cors import CORSMiddleware
from v1.di import init_di
from decouple import config
# # from starlette.middleware import Middleware

desc = """
Developers:\n
    + Dang Pham (Backend)
    + Kien Duong (Frontend)
Hotlines:\n
    + 911
"""
tags_metadata = [
    {
        "name": "Authentication",
        "description": "Support for the signup, login, logout function",
    },
    {
        "name": "kkk",
        "description": "Only God knows why I'm here",
    },
]

app = FastAPI(
    title='APIs for The Social Hub',
    description=desc,
    version='1',
    openapi_tags=tags_metadata,
    docs_url="/docs", redoc_url="/redoc")

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

init_di()

from v1.routers import authentication, db_es

app.include_router(authentication.router)
app.include_router(db_es.router)


