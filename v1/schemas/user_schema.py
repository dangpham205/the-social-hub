from pydantic import BaseModel, validator, Field, conint, Json, EmailStr
from typing import List, Any
from cores.helpers import helper
from datetime import datetime, date
from enum import Enum
from enums.db import model_enum
from fastapi import HTTPException
import re


class UpdateProfileSchema(BaseModel):
    # username: str = None
    full_name: str = None
    phone: str = None
    bio: str = None
    dob: date = None
    gender: model_enum.GenderEnum = None
    location: str = None
    # email: str
    
    # @validator('username')
    # def username_validation(cls, v):
    #     # 1 to 30 characters that are either letters (uppercase or lowercase), digits, underscores, or periods. 
    #     if v:
    #         regex = r'^[a-z0-9_\.]{1,25}$'
    #         if not re.match(regex, v) or v.endswith('.') or v.startswith('.') : 
    #             raise ValueError("Username invalid. Username can contains numerics, alphabetical characters (lowercase), dots and underscores. Can't start or end with dot")
    #     return v
    
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                # 'username': 'usernam._e',
                'full_name': 'Hai Danger',
                'phone': '+123123',
                'bio': 'i am a god',
                'dob': '2023-03-03',
                'gender': 'Male',
                'location': 'Ho Chi Minh',
            }
        }
        
        
class UpdateAvatarSchema(BaseModel):
    avatar: str

class UpdateAvatar2ndSchema(BaseModel):
    avatar_2nd: str