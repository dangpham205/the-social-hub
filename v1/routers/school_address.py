from fastapi import APIRouter, status, HTTPException, Depends, Request, UploadFile, File
from fastapi.responses import StreamingResponse
from typing import Any
from cores.elasticsearch.es_helper import ElasticSearch
from v1.schemas.school_address_schema import SchoolAddressResponse, SchoolAddressCreateRequest, SchoolAddressUpdateRequest
from repositories.services.school_address_service import SchoolAddressService
from cores.helpers.paging import Page, PaginationParams
from cores.schemas.sche_base import DataResponse
from cores.logging import logger
from cores.databases.connection import get_db
from sqlalchemy.orm import Session
from cores.authorization import authorization_helper
from cores.rabbitmq.rpc_client import FibonacciRpcClient
# from workers.school_worker import SchoolProducer
from enums.elasticsearch import es_enum
from enums.db import table_enum
from enums.workers.worker_enum import MYSQL_QUEUE
from v1.es_queries import q_school

router = APIRouter(
    # dependencies=[Depends(authorization_helper.check_access)],
    prefix='/school-addresses',
    tags=['School Addresses'],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}}
)

  # Create the tables.

@router.get('/{id}', status_code=status.HTTP_200_OK,
            # , response_model=DataResponse[SchoolResponse]
            )
async def show(id: int, db: Session = Depends(get_db)):
    # service = SchoolConcrete().service
    # data = service.find(db, id)
    data = ElasticSearch().get_a_document(es_enum.INDEX_SCHOOL_ADDRESS, id)
    result = {}
    if data['found'] == True:
        result = data['_source']
    return DataResponse().success_response(result)

@router.get('/', status_code=status.HTTP_200_OK
    , response_model=Page[SchoolAddressResponse]
            )
async def paginate(school_id: int = None, params: PaginationParams = Depends(), db: Session = Depends(get_db)) -> Any:
    query = None
    if school_id:
        query = {
            "match": {
                'school_id': school_id
            }
        }
    page = params.page
    page_size = params.page_size
    sort_by = params.sort_by
    order = params.order
    data = ElasticSearch().paginate(
        index_name=es_enum.INDEX_SCHOOL_ADDRESS, 
        query=query,
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        order=order
    )
    data['code'] = 200
    data['message'] = True
    for address in data["data"]:
        name, code= q_school.school_info_by_school_id(address['school_id'])
        address['school_name'] = name
        address['school_code'] = code 
    return data

@router.post('/', status_code=status.HTTP_201_CREATED)
async def store(req: Request, request: SchoolAddressCreateRequest, db: Session = Depends(get_db)):
    FibonacciRpcClient().send_message(
        method='post', 
        header={
            "table": table_enum.TABLE_SCHOOL_ADDRESS,
            "request_state": req.state.__dict__,
        },
        routing_key=MYSQL_QUEUE, 
        body=dict(request)
    )
    return DataResponse().success_response(data=request)

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
async def update(req: Request, id: int, request: SchoolAddressUpdateRequest, db: Session = Depends(get_db)):
    data = dict(request)
    data['id'] = id
    FibonacciRpcClient().send_message(
        method='put', 
        header={
            "table": table_enum.TABLE_SCHOOL_ADDRESS,
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
            "table": table_enum.TABLE_SCHOOL_ADDRESS,
            "request_state": req.state.__dict__,
        },
        routing_key=MYSQL_QUEUE, 
        body=id
    )
    return DataResponse().success_response(data=id)





# @router.post('/', status_code=status.HTTP_201_CREATED)
# async def store(request: SchoolAddressCreateRequest, db: Session = Depends(get_db)):
#     service = SchoolAddressService()
#     result = service.repo.create(db, request)
#     # FibonacciRpcClient('', ROUTING_KEY).call(result.id)
#     return DataResponse().success_response(data=result)

# @router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
# async def update(id: int, request: SchoolAddressUpdateRequest, db: Session = Depends(get_db)):
#     service = SchoolAddressService()
#     result = service.repo.update(db, id, request)
#     return DataResponse().success_response(data=result)

# @router.delete('/{id}', status_code=status.HTTP_202_ACCEPTED)
# async def destroy(id: int, db: Session = Depends(get_db)):
#     try:
#         service = SchoolAddressService()
#         result = service.repo.delete(db, id)
#         return DataResponse().success_response(data=result)
#     except Exception as e:
#         return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=logger.error(e))
    
# @router.get('/{id}', status_code=status.HTTP_200_OK,
#             # , response_model=DataResponse[SchoolResponse]
#             )
# async def show(id: int, db: Session = Depends(get_db)):
#     service = SchoolAddressConcrete().service
#     data = service.find(db, id)
#     return DataResponse().success_response(data)

# @router.get('/', status_code=status.HTTP_200_OK
#     , response_model=Page[SchoolAddressResponse]
#             )
# async def paginate(request: Request, params: PaginationParams = Depends(), db: Session = Depends(get_db)) -> Any:
#     try:
#         service = SchoolAddressService()
#         data = service.repo.paginate(db, params)
#         return data
#     except Exception as e:
#         return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=logger.error(e))