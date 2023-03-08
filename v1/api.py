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
Error codes:\n
    + https://github.com/dawnnywhereyouat/the-social-hub/blob/main/error_codes.py
"""
tags_metadata = [
    {
        "name": "Authentication",
        "description": "Support for the signup, login, logout function",
    },
    {
        "name": "User",
        "description": "Features for users: update profile, follow,...",
    },
    {
        "name": "Post",
        "description": "Create / Update / Delete post, get Posts for feed",
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

from v1.routers import authentication, db_es, user, post

app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(post.router)
app.include_router(db_es.router)


