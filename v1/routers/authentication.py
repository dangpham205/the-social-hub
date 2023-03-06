from fastapi import APIRouter, status, HTTPException, Depends, Request, UploadFile, File
from cores.schemas.sche_base import DataResponse
from v1.schemas import authentication_schema
from cores.helpers import helper
from services.authentication_service import SignUpService, LoginService, TokenService
from utils.util_funcs import return_status_codes

router = APIRouter(
    # dependencies=[Depends(authorization_helper.check_access)],
    prefix='/authentication',
    tags=['Authentication'],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}}
)

desc_signup = f"""Create unverified account\n
    {return_status_codes('200', '500', '501', '502')}
"""
desc_signup_verify = f"""Create unverified account\n
    {return_status_codes('200', '500', '503', '504', '505')}
"""
desc_resend_verify = f"""Resend verification email\n
    {return_status_codes('200', '500', '502')}
"""
desc_login = f"""Login\n
    {return_status_codes('200', '500', '506', '507', '508')}
"""

@router.post('/signup', description=desc_signup)
async def signup(obj: authentication_schema.SignUpBase):
    signup = SignUpService(info=obj)
    info_valid = signup.verify_signup_info()
    if not info_valid[0]:
        return DataResponse().custom_response(500, False, f"{info_valid[1]} already exists")
    unverified_user =  signup.write_unverified_user()
    if not unverified_user:
        return DataResponse().custom_response(501, False, f"Create new user failed! Please try again later.")
    token = signup.generate_confirm_token(unverified_user.id)
    send_email_success = signup.send_confirm_email(token=token)
    if not send_email_success:
        return DataResponse().custom_response(502, False, f"Something went wrong! Please try again later.")
    
    return DataResponse().success_response('Please check your email')

@router.post('/signup-verify', description=desc_signup_verify)
async def signup_verify(token: str):
    signup = SignUpService()
    result = signup.verify_user_account(token=token)
    return result

@router.post('/resend-verify', description=desc_resend_verify)
async def resend_verify(email: str):
    signup = SignUpService()
    uid = signup.get_uid_by(email=email)
    if not uid:
        return DataResponse().custom_response(500, False, f"Something went wrong! Please try again later.")
    token = signup.generate_confirm_token(id=uid)
    send_email_success = signup.send_confirm_email(token=token, recipients=[email])
    if not send_email_success:
        return DataResponse().custom_response(502, False, f"Something went wrong! Please try again later.")
    return DataResponse().success_response('Please check your email')
    

@router.post('/login', description=desc_login)
async def login(obj: authentication_schema.LoginBase):
    login = LoginService(info=obj)
    uid = login.get_uid()
    if not uid:
        return DataResponse().custom_response(506, False, f"Unregistered email/username! Please signup.")
    is_user_verified = login.check_user_verified(uid)
    if not is_user_verified: 
        return DataResponse().custom_response(508, False, f"Your account is not verified.")
    verify_password = login.verify_password(uid=uid)
    if not verify_password:
        return DataResponse().custom_response(507, False, f"Wrong password! Please try again.")
    user_token = TokenService(uid=uid).generate_user_token(long_live=obj.remember_me)
    return DataResponse().success_response('Login success', token=user_token)

@router.post('/-----------------------------------------------')
async def below_not_done(token: str):
    return 1

@router.post('/request-reset-password')
async def request_reset_password(email: str):
    return 1

@router.post('/reset-password')
async def reset_password(token: str, new_pass: str):
    return 1
        
        
    