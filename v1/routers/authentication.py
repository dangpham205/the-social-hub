from fastapi import APIRouter, status, HTTPException, Depends, Request, UploadFile, File
from cores.schemas.sche_base import DataResponse
from v1.schemas import authentication_schema
from cores.helpers import helper
from services.authentication_service import signup_service
from utils.util_funcs import return_status_codes

router = APIRouter(
    # dependencies=[Depends(authorization_helper.check_access)],
    prefix='/authentication',
    tags=['Authentication'],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}}
)

desc_signup = f"""Create unverified account\n
    {return_status_codes('200', '500', '501')}
"""
desc_signup_verify = f"""Create unverified account\n
    {return_status_codes('200', '500', '503', '504', '505')}
"""

@router.post('/signup', description=desc_signup)
async def signup(obj: authentication_schema.SignUpBase):
    signup = signup_service.SignUpService(info=obj)
    info_valid = signup.verify_signup_info()
    if not info_valid[0]:
        return DataResponse().custom_response(500, False, f"{info_valid[1]} already exists")
    unverified_user =  signup.write_unverified_user()
    if not unverified_user:
        return DataResponse().custom_response(501, False, f"Create new user failed! Please try again later.")
    token = signup.generate_confirm_token(unverified_user.id)
    send_email_success = signup.send_confirm_email(token=token)
    # if not send_email_success:
    #     return DataResponse().custom_response(502, False, f"Create new user failed! Please try again later.")
    
    return DataResponse().success_response('Please check your email')

@router.post('/signup-verify', description=desc_signup_verify)
async def signup_verify(token: str):
    signup = signup_service.SignUpService()
    result = signup.verify_user_account(token=token)
    return result

@router.post('/resend-verify', description='Resend verification email')
async def resend_verify(email: str):
    signup = signup_service.SignUpService()
    uid = signup.get_uid_by_email(email=email)
    token = signup.generate_confirm_token(id=uid)
    send_email_success = signup.send_confirm_email(token=token, recipients=[email])
    # if not send_email_success:
    #     return DataResponse().custom_response(502, False, f"Create new user failed! Please try again later.")
    return DataResponse().success_response('Please check your email')
    

@router.post('/login', description='Login')
async def login(obj: authentication_schema.LoginBase):
    return 1

@router.post('/logout')
async def show(token: str):
    return 1
        
        
    