from pydantic import BaseModel, validator, Field, conint, Json
from typing import List, Any
from cores.helpers import helper
from datetime import datetime
from enum import Enum


class TypeEnum(Enum):
    news = "NEWS"
    megastory = "MEGASTORY"

class SchoolLinkBase(BaseModel):
    school_id: int
    link: str
    class Config:
        orm_mode = True


class SchoolLinkResponse(SchoolLinkBase):
    id: int
    thumb: str 
    title: str 
    type: TypeEnum 
    school_name: str | None
    school_code: str | None
    # view: int
    # list_criteria_user_group: List[Any] = []
    created_at: datetime | None
    updated_at: datetime | None
    deleted_at: datetime | None


class SchoolLinkCreateRequest(SchoolLinkBase):
    pass


class SchoolLinkUpdateRequest(SchoolLinkBase):
    pass
    # class Config:
    #     orm_mode = True
    #     schema_extra = {
    #
    #     }
