from pydantic import BaseModel, validator, Field, conint, Json
from typing import List, Any
from cores.helpers import helper
from datetime import datetime
from enum import Enum


class TypeEnum(Enum):
    news = "NEWS"
    megastory = "MEGASTORY"

class SchoolBase(BaseModel):
    school_id: int
    link: str
    class Config:
        orm_mode = True


class SchoolLinkResponse(SchoolBase):
    id: int
    thumb: str 
    title: str 
    type: TypeEnum 
    avatar: Json | None
    school_name: str | None
    school_code: str | None
    # view: int
    # list_criteria_user_group: List[Any] = []
    created_at: datetime | None
    updated_at: datetime | None
    deleted_at: datetime | None


class SchoolCreateRequest(SchoolBase):
    class Config:
        schema_extra = {
            "example": {
                "code": "string",
                "name": "string",
                "targets": 0,
                "phone": "string",
                "email": "string",
                "logo": "string",
                "avatar": "\"string gi do \"",
                "website": "string",
                "description": "string",
                "seo_description": "string",
                "vision": "string",
                "mission": "string",
                "enrollment_targets": 0,
                "method_content": "string",
                "is_outstanding": False,
                "order": 0
            }
        }


class SchoolUpdateRequest(SchoolBase):
    class Config:
        schema_extra = {
            "example": {
                "code": "string",
                "name": "string",
                "targets": 0,
                "phone": "string",
                "email": "string",
                "logo": "string",
                "avatar": "\"string gi do \"",
                "website": "string",
                "description": "string",
                "seo_description": "string",
                "vision": "string",
                "mission": "string",
                "enrollment_targets": 0,
                "method_content": "string",
                "is_outstanding": False,
                "order": 0
            }
        }
