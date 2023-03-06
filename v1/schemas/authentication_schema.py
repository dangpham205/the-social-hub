from pydantic import BaseModel, validator, Field, conint, Json, EmailStr
from typing import List, Any
from cores.helpers import helper
from datetime import datetime, date
from enum import Enum
from enums.db import model_enum
import re

class SignUpBase(BaseModel):
    username: str
    email: str
    full_name: str
    phone: str
    dob: date
    gender: model_enum.GenderEnum
    password: str
    password_confirm: str

    @validator('email')
    def email_must_contain_at(cls, v):
        if "@" not in v or v.endswith('@'):
            raise ValueError("Email invalid")
        return v
    
    @validator('username')
    def username_validation(cls, v):
        # 1 to 30 characters that are either letters (uppercase or lowercase), digits, underscores, or periods. 
        regex = r'^[a-z0-9_\.]{1,25}$'
        if not re.match(regex, v) or v.endswith('.') or v.startswith('.') : 
            raise ValueError("Username invalid. Username can contains numerics, alphabetical characters (lowercase), dots and underscores. Can't start or end with dot")
        return v

    @validator('phone')
    def phone_validation(cls, v):
        # 1 to 30 characters that are either letters (uppercase or lowercase), digits, underscores, or periods. 
        regex = r'^[0-9+]{1,15}$'
        regex2 = r'^[0-9]{1,15}$'
        if not re.match(regex, v) or not re.match(regex2, v[1:]): 
            raise ValueError("Phone number invalid")
        return v

    @validator('password_confirm')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                'username': 'usernam._e',
                'email': 'sdasd@example.com',
                'full_name': 'Hai Danger',
                'phone': '+123123',
                'dob': '2023-03-03',
                'gender': 'Male',
                'password': 'pass',
                'password_confirm': 'pass',
            }
        }
        
class LoginBase(BaseModel):
    user: str
    password: str
    remember_me: bool = False
    

