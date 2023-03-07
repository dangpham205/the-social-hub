from fastapi import APIRouter, status, HTTPException, Depends, Request, UploadFile, File
from cores.schemas.sche_base import DataResponse
from v1.schemas import user_schema
from cores.helpers import helper
from utils.util_funcs import return_status_codes
from cores.authen.auth_bearer import JWTBearer
from decorators.refresh_token import refresh_token
from services.temp_service import UserService

router = APIRouter(
    prefix='/post',
    tags=['Post'],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
    # dependencies=[Depends(JWTBearer())],
)

@router.get('/create/', description='đấ')
@refresh_token
async def create_post(uid: int, user_token=Depends(JWTBearer())):
    pass