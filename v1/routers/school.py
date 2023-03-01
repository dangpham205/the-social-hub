import json
from fastapi import APIRouter, status, HTTPException, Depends, Request, UploadFile, File
from fastapi.responses import StreamingResponse
from typing import Any
from v1.schemas.school_schema import SchoolResponse, SchoolCreateRequest, SchoolUpdateRequest
from repositories.services.school_service import SchoolService
from cores.helpers.paging import Page, PaginationParams
from cores.schemas.sche_base import DataResponse
from cores.logging import logger
from cores.databases.connection import get_db
from sqlalchemy.orm import Session
from cores.authorization import authorization_helper
from cores.rabbitmq.rpc_client import FibonacciRpcClient
# from workers.school_worker import SchoolProducer
from data_providers.school.school_concrete import SchoolConcrete
from enums.workers.worker_enum import KEY_API_SCHOOL, EXCHANGE_API, MYSQL_QUEUE
from cores.elasticsearch.es_helper import ElasticSearch
from enums.elasticsearch import es_enum
from enums.db import table_enum
from v1.es_queries import q_school

router = APIRouter(
    # dependencies=[Depends(authorization_helper.check_access)],
    prefix='/schools',
    tags=['Schools'],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}}
)

@router.get('/{id}', status_code=status.HTTP_200_OK,
            # , response_model=DataResponse[SchoolResponse]
            )
async def show(id: int, db: Session = Depends(get_db)):
    # service = SchoolConcrete().service
    # data = service.find(db, id)
    data = ElasticSearch().get_a_document(es_enum.INDEX_SCHOOL, id)
    result = {}
    if data['found'] == True:
        result = data['_source']
    return DataResponse().success_response(result)

@router.get('/', status_code=status.HTTP_200_OK
    , response_model=Page[SchoolResponse]
            )
async def paginate(name: str = None, province_id: int = None, code : str = None, 
                   params: PaginationParams = Depends(), db: Session = Depends(get_db)) -> Any:
    # Cơ chế paginate của school:
    # Nếu có search theo tỉnh thành (province_id) thì search ra list id tất cả các trường thuộc province_id đó
    # Sau đó mới bắt đầu filter tiếp theo name, code, ...
    # Và cuối cùng là paginate (size, sort, order)
    query = q_school.paginate_school(
        province_id=province_id,
        name=name,
        code=code
    )
    page = params.page
    page_size = params.page_size
    sort_by = params.sort_by
    order = params.order
    data = ElasticSearch().paginate(
        index_name=es_enum.INDEX_SCHOOL, 
        query=query,
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        order=order
    )
    data['code'] = 200
    data['message'] = True 
    for school in data["data"]:
        total_majors= q_school.total_enrollment_informations_by_school_id(school['id'])
        address_default_province = q_school.address_default_province_name_by_school_id(school['id'])
        school['address_default_province'] = address_default_province
        school['total_majors'] = total_majors 
    return data

@router.post('/', status_code=status.HTTP_201_CREATED)
async def store(req: Request, request: SchoolCreateRequest, db: Session = Depends(get_db)):
    #
    FibonacciRpcClient().send_message(
        method='post', 
        header={
            "table": table_enum.TABLE_SCHOOL,
            "request_state": req.state.__dict__,
        },
        routing_key=MYSQL_QUEUE, 
        body=dict(request)
    )
    return DataResponse().success_response(data=request)

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
async def update(req: Request, id: int, request: SchoolUpdateRequest, db: Session = Depends(get_db)):
    data = dict(request)
    data['id'] = id
    FibonacciRpcClient().send_message(
        method='put', 
        header={
            "table": table_enum.TABLE_SCHOOL,
            "request_state": req.state.__dict__,
        },
        routing_key=MYSQL_QUEUE, 
        body=data
    )
    return DataResponse().success_response(data=data)

@router.delete('/{id}', status_code=status.HTTP_202_ACCEPTED)
async def destroy(req: Request, id: int, db: Session = Depends(get_db)):
    FibonacciRpcClient().send_message(
        method='delete', 
        header={
            "table": table_enum.TABLE_SCHOOL,
            "request_state": req.state.__dict__,
        },
        routing_key=MYSQL_QUEUE, 
        body=id
    )
    return DataResponse().success_response(data=id)
