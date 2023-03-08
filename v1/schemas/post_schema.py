from pydantic import BaseModel, validator, Field, conint, Json, EmailStr
from typing import List, Any
from cores.helpers import helper
from datetime import datetime, date
from enum import Enum
from enums.db import model_enum
from fastapi import HTTPException
import re


class CreatePostSchema(BaseModel):
    user_id: int
    content: str
    picture: str
    
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                'user_id': 2,
                'content': 'sharingsomething',
                'picture': 'path'
            }
        }