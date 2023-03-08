from fastapi import APIRouter, status, HTTPException, Depends, Request, UploadFile, File
from cores.schemas.sche_base import DataResponse
from decouple import config
from sqlalchemy import create_engine
from db import Base
from sqlalchemy.pool import NullPool
from v1.es_mappings import user
from error_codes import get_code_detail

router = APIRouter(
    # dependencies=[Depends(authorization_helper.check_access)],
    prefix='/justdont',
    tags=['kkk'],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}}
)

@router.get('/list_endpoints/')
def list_endpoints(request: Request):
    url_list = [
        {'path': route.path, 'name': route.name}
        for route in request.app.routes
    ]
    return url_list

@router.get('/code/')
def error_code(code: int):
    return get_code_detail(code=code)

@router.get('/create_tables')
def create_tables(password: str):
    if password == '123':
        _host = config('db_host')
        _username = config('db_username')
        _password = config('db_password') 
        _database = config('db_database')
        engine = create_engine(
            f'mysql+pymysql://{_username}:{_password}@{_host}/{_database}?charset=utf8mb4', echo=False, poolclass=NullPool, isolation_level="READ UNCOMMITTED")
        Base.metadata.create_all(engine)
        return 'OK'
    else: 
        return 'No'

@router.get('/drop_db')
def create_tables(password: str):
    if password == '123':
        _host = config('db_host')
        _username = config('db_username')
        _password = config('db_password') 
        _database = config('db_database')
        engine = create_engine(
            f'mysql+pymysql://{_username}:{_password}@{_host}/{_database}?charset=utf8mb4', echo=False, poolclass=NullPool, isolation_level="READ UNCOMMITTED")
        Base.metadata.drop_all(engine)
        return 'OK'
    else: 
        return 'No'
    
# @router.get('/create_es')
# def create_es(password: str):
#     if password == '123':
#         from cores.elasticsearch.es_helper import ElasticSearch
#         from cores.elasticsearch import es_base
#         from enums.db import table_name_enum
#         es = ElasticSearch()
#         indices = [
#             table_name_enum.USER,
#         ]
#         mappings = [
#             user.mapping,
#             # link_mapping.mapping
#         ]
#         for index, mapping in zip(indices, mappings):
#             try:
#                 if es.check_index_is_exists(index):
#                     es.delete_index(index)
#                 if mapping:
#                     index_setting = es_base.get_setting_to_create_index(mapping)
#                 else:
#                     index_setting = None
#                 es.create_index(index_name=index, index_body=index_setting)
#             except Exception as e: 
#                 print(f'index {index}:: {e}')
#                 pass
#         return 'OK'
#     else: 
#         return 'No'