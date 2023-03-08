from fastapi import APIRouter, status, HTTPException, Depends, Request, UploadFile, File
from cores.schemas.sche_base import DataResponse
from v1.schemas import user_schema
from cores.helpers import helper
from utils.util_funcs import return_status_codes
from cores.authen.auth_bearer import JWTBearer
from decorators.refresh_token import refresh_token
from services.temp_service import UserService

router = APIRouter(
    prefix='/user',
    tags=['User'],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
    # dependencies=[Depends(JWTBearer())],
)

desc_get_profile = f"""Get user info\n
    {return_status_codes('200', '500')}
"""

desc_update_profile = f"""Update user info\n
    {return_status_codes('200', '500', '405', '501')}
"""
desc_avt_profile = f"""Update user avatar\n
    {return_status_codes('200', '500', '405', '501')}
"""
desc_avt2_profile = f"""Update user cover photo\n
    {return_status_codes('200', '500', '405', '501')}
"""
desc_post_profile = f"""Get user's posts\n
    {return_status_codes('200', '500', '405', '501')}
"""

@router.get('/profile/me', description=desc_get_profile)
@refresh_token
async def get_my_profile(user_token=Depends(JWTBearer())):
    user = UserService(user_token=user_token)
    data = user.get_my_profile()
    return data

@router.get('/profile/{uid}', description=desc_get_profile)
@refresh_token
async def get_profile(uid: int, user_token=Depends(JWTBearer())):
    user = UserService(user_token=user_token, uid=uid)
    data = user.get_profile()
    return data

@router.patch('/update-profile/{uid}', description=desc_update_profile)
@refresh_token
async def update_profile(uid: int, obj: user_schema.UpdateProfileSchema, user_token=Depends(JWTBearer())):
    user = UserService(user_token=user_token, uid=uid)
    data = user.update_profile(info=obj)
    return data

@router.post('/update-avatar/{uid}', description=desc_avt_profile)
@refresh_token
async def update_avatar(uid: int, obj: user_schema.UpdateAvatarSchema, user_token=Depends(JWTBearer())):
    user = UserService(user_token=user_token, uid=uid)
    data = user.update_avatar(**obj.dict())
    return data

@router.post('/update-avatar2nd/{uid}', description=desc_avt2_profile)
@refresh_token
async def update_cover(uid: int, obj: user_schema.UpdateAvatar2ndSchema, user_token=Depends(JWTBearer())):
    user = UserService(user_token=user_token, uid=uid)
    data = user.update_avatar(**obj.dict())
    return data

@router.get('/posts/{uid}', description=desc_post_profile)
@refresh_token
async def get_user_posts(uid: int, user_token=Depends(JWTBearer())):
    user = UserService(user_token=user_token, uid=uid)
    data = user.get_profile_posts()
    return data