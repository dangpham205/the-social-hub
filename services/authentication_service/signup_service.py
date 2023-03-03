from db import User
from sqlalchemy import or_
from cores.databases.connection import get_db
from repositories.services.user_service import UserService

class SignUpService():
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
        
        # data = User(**self.info.dict())
        try:
            service = UserService()
            result = service.repo.create(self.session, self.info.dict())
            return result
        except:
            
            raise