from fastapi import APIRouter, status, HTTPException, Depends, Request, UploadFile, File
from cores.schemas.sche_base import DataResponse
from v1.schemas import authentication_schema
from cores.helpers import helper
from services.authentication_service import signup_service

router = APIRouter(
    # dependencies=[Depends(authorization_helper.check_access)],
    prefix='/authentication',
    tags=['Authentication'],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}}
)

@router.post('/signup')
async def show(obj: authentication_schema.SignUpBase):
    signup = signup_service.SignUpService(info=obj)
    info_valid = signup.verify()
    if not info_valid[0]:
        print(info_valid[1])
        return DataResponse().custom_response(500, False, f"{info_valid[1]} already exists")
    unverified_user =  signup.write_unverified_user()
    if not unverified_user:
        pass
    token = signup.generate_confirm_token(unverified_user.id)
    
    result = token
    return DataResponse().success_response(result)
        
    