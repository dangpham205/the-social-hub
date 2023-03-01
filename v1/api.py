from fastapi import FastAPI, APIRouter, Request
from v1.routers import school, school_address, school_staff

from fastapi.middleware.cors import CORSMiddleware
from v1.di import init_di
from v1.es_mappings import school_mapping

# # from starlette.middleware import Middleware
#
desc = """
# Api For School Service
# """
tags_metadata = [
    {
        "name": "hehe1",
        "description": "desc",
    },
    {
        "name": "hehe2",
        "description": "desc",
    },
]

app = FastAPI(
    title='API For hehe',
    description=desc,
    version='1',
    openapi_tags=tags_metadata,
    docs_url="/docs", redoc_url="/redoc")

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
init_di()

app.include_router(school.router)
app.include_router(school_address.router)
app.include_router(school_staff.router)

router = APIRouter(
    prefix="/utils",
    tags=["utilities"]
)

@router.get('/list_endpoints/')
def list_endpoints(request: Request):
    url_list = [
        {'path': route.path, 'name': route.name}
        for route in request.app.routes
    ]
    return url_list
from decouple import config
from sqlalchemy import create_engine
from db import Base
from sqlalchemy.pool import NullPool

@router.get('/create_tables')
def create_tables(password: str):
    if password == 'password123':
        _host = config('db_host')
        _username = config('db_username')
        _password = config('db_password') 
        # _database = config('db_database_test')
        _database = 'school_service'
        engine = create_engine(
            f'mysql+pymysql://{_username}:{_password}@{_host}/{_database}?charset=utf8mb4', echo=False, poolclass=NullPool, isolation_level="READ UNCOMMITTED")
        Base.metadata.create_all(engine)
        return 'OK'
    else: 
        return 'No'
    
@router.get('/create_es')
def create_es(password: str):
    if password == 'password123':
        from cores.elasticsearch.es_helper import ElasticSearch
        from enums.elasticsearch import es_enum
        from cores.elasticsearch import es_base
        es = ElasticSearch()
        indices = [
            es_enum.INDEX_SCHOOL,
            es_enum.INDEX_SCHOOL_ADDRESS,
            es_enum.INDEX_SCHOOL_CATEGORY,
            es_enum.INDEX_SCHOOL_ENROLL_INFORMATION,
            es_enum.INDEX_SCHOOL_INFRASTRUCTURE,
            es_enum.INDEX_SCHOOL_NEWS,
            es_enum.INDEX_SCHOOL_POST,
            es_enum.INDEX_SCHOOL_STAFF,
            es_enum.INDEX_SCHOOL_LINK
        ]
        mappings = [
            school_mapping.mapping,
            # link_mapping.mapping
        ]
        for index, mapping in zip(indices, mappings):
            try:
                if es.check_index_is_exists(index):
                    es.delete_index(index)
                if mapping:
                    index_setting = es_base.get_setting_to_create_index(mapping)
                else:
                    index_setting = None
                es.create_index(index_name=index, index_body=index_setting)
            except Exception as e: 
                print(f'index {index}:: {e}')
                pass
        return 'OK'
    else: 
        return 'No'
app.include_router(router)