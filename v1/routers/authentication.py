from fastapi import APIRouter, status, HTTPException, Depends, Request, UploadFile, File
from cores.schemas.sche_base import DataResponse
from v1.schemas import authentication_schema
from cores.databases.connection import get_db
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


from db import User
from sqlalchemy import or_
class SignUp():
    def __init__(self, info):
        self.session = next(get_db())
        self.info = info

    def verify(self):
        duplicate_user = self.session.query(User).filter(or_(
                User.username == self.info.username,
                User.email == self.info.email,
            )).first()
        if duplicate_user:
            return False
        
        data = User(**self.info.dict())
        if hasattr(User, 'created_at') and str(User.created_at.type) == 'INTEGER':
                current_time = helper.get_current_time_as_int()
                data.created_at = current_time
                data.updated_at = current_time
        try:
            self.session.add(data)
            self.session.commit()
            self.session.refresh(data)
            return data
        except:
            self.session.rollback()
            raise
        
    