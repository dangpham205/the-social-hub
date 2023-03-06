from pydantic import BaseModel
from typing import Generic, TypeVar, Optional, List
from pydantic.generics import GenericModel
from fastapi import Query, Depends, FastAPI
from pydantic.dataclasses import dataclass
T = TypeVar("T")

class ResponseSchemaBase(BaseModel):
    __abstract__ = True

    code: int = None
    success: bool = None

    def custom_response(self, code: int, success: bool):
        self.code = code
        self.success = success
        return self

    def success_response(self):
        self.code = 200
        self.success = True
        return self

class DataResponse(ResponseSchemaBase, GenericModel, Generic[T]):
    data: Optional[T] = None
    token: str = None

    class Config:
        arbitrary_types_allowed = True

    def custom_response(self, code: int, success: bool, data: T, token=None):
        self.code = code
        self.success = success
        self.data = data
        self.token = token
        return self

    def success_response(self, data: T, token=None):
        self.code = 200
        self.success = True
        self.data = data
        self.token = token
        return self

class MetadataSchema(BaseModel):
    current_page: int
    page_size: int
    total_items: int

@dataclass
class QueryParams:
    req1: float = Query(...)
    opt1: int = Query(None)
    req_list: List[str] = Query(...)
