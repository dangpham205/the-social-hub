from fastapi import APIRouter, status, HTTPException, Depends, Request, UploadFile, File
from cores.schemas.sche_base import DataResponse
from v1.schemas import authentication_schema
from cores.helpers import helper
from services.authentication_service import SignUpService, LoginService, TokenService
from utils.util_funcs import return_status_codes

router = APIRouter(
    # dependencies=[Depends(authorization_helper.check_access)],
    prefix='/user',
    tags=['User'],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}}
)

@router.get('/profile', description='dsadsa')
async def get_profile(obj: authentication_schema.SignUpBase):
    pass

@router.post('/update-profile', description='dsadsa')
async def update_profile(obj: authentication_schema.SignUpBase):
    pass

@router.post('/update-avatar', description='dsadsa')
async def update_avatar(obj: authentication_schema.SignUpBase):
    pass

@router.post('/update-cover', description='dsadsa')
async def update_cover(obj: authentication_schema.SignUpBase):
    pass

@router.post('/follow', description='dsadsa')
async def follow(obj: authentication_schema.SignUpBase):
    pass