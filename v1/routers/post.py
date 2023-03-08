from fastapi import APIRouter, status, HTTPException, Depends, Request, UploadFile, File
from cores.schemas.sche_base import DataResponse
from v1.schemas import post_schema
from cores.helpers import helper
from utils.util_funcs import return_status_codes
from cores.authen.auth_bearer import JWTBearer
from decorators.refresh_token import refresh_token
from services.temp_service import PostService

router = APIRouter(
    prefix='/post',
    tags=['Post'],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
    # dependencies=[Depends(JWTBearer())],
)

desc_create_post = f"""Create post\n
    {return_status_codes('200', '500', '405')}
"""

@router.post('/create', description=desc_create_post)
@refresh_token
async def create_post(obj: post_schema.CreatePostSchema, user_token=Depends(JWTBearer())):
    post_service = PostService(user_token=user_token)
    data = post_service.create_post(post=obj)
    return data 

@router.delete('/delete/{id}', description=desc_create_post)
@refresh_token
async def create_post(id: int, user_token=Depends(JWTBearer())):
    post_service = PostService(user_token=user_token)
    data = post_service.delete_post(id=id)
    return data 

from fastapi.responses import JSONResponse
# error_response = JSONResponse(content={"detail": "Item not found"}, status_code=400)
#         # Raise the custom JSON response
#         raise error_response