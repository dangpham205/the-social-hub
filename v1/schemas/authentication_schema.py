from pydantic import BaseModel, validator, Field, conint, Json
from typing import List, Any
from cores.helpers import helper
from datetime import datetime, date
from enum import Enum
from enums.db import model_enum

class GenderEnum(Enum):
    male = model_enum.gender_male
    female = model_enum.gender_female
    other = model_enum.gender_other

class SignUpBase(BaseModel):
    class Config:
        orm_mode = True
    username: str
    email: str
    full_name: str
    phone: str
    dob: date
    gender: GenderEnum