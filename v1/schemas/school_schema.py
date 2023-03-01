from pydantic import BaseModel, validator, Field, conint, Json
from typing import List, Any
from cores.helpers import helper
from datetime import datetime


class SchoolBase(BaseModel):
    code: str
    name: str
    targets: int
    phone: str | None
    email: str | None
    logo: str | None
    avatar: Json | None
    website: str | None
    description: str | None
    seo_description: str | None
    vision: str | None
    mission: str | None
    enrollment_targets: int | None
    method_content: str | None
    is_outstanding: bool = False
    order: int | None

    class Config:
        orm_mode = True


class SchoolResponse(SchoolBase):
    id: int
    # view: int
    state: str
    avatar: Any | None
    address_default_province: str | None
    total_majors: int | None
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
