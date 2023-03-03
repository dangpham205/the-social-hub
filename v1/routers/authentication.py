from fastapi import APIRouter, status, HTTPException, Depends, Request, UploadFile, File
from cores.schemas.sche_base import DataResponse
from v1.schemas import authentication_schema
from cores.helpers import helper

router = APIRouter(
    # dependencies=[Depends(authorization_helper.check_access)],
    prefix='/authentication',
    tags=['Authentication'],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}}
)

@router.post('/signup')
async def show(obj: authentication_schema.SignUpBase):
    signup = SignUp(info=obj)
    result = signup.verify()
    return DataResponse().success_response(result)



        
    