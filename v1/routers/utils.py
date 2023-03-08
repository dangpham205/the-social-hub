from fastapi import APIRouter, status, HTTPException, Depends, Request, UploadFile, File
from error_codes import get_code_detail


router = APIRouter(
    prefix='/utils',
    tags=['Utils'],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
    # dependencies=[Depends(JWTBearer())],
)


@router.get('/code')
def error_code(code: int):
    return get_code_detail(code=code)