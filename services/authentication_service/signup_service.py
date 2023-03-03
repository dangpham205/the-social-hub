from db import User
from sqlalchemy import or_
from cores.databases.connection import get_db
from repositories.services import UserService
from cores.authen import signJWT
import datetime

class SignUpService():
    def __init__(self, info):
        self.session = next(get_db())
        self.info = info

    def verify(self):
        # duplicate_user = self.session.query(User).filter(or_(
        #         User.username == self.info.username,
        #         User.email == self.info.email,
        #     )).first()
        duplicate_user_username = self.session.query(User).filter(User.username == self.info.username).first()
        duplicate_user_email = self.session.query(User).filter(User.email == self.info.email).first()
        if duplicate_user_username:
            return False, 'Username'
        if duplicate_user_email:
            return False, 'Email'
        return True, None

    def write_unverified_user(self):
        try:
            service = UserService()
            result = service.repo.create(self.session, self.info)
            return result
        except Exception:
            return None
    
    def generate_confirm_token(self, id):
        expires_at = datetime.datetime.now() + datetime.timedelta(seconds=600)
        info = {
            'id': id,
            'expires_at': expires_at.isoformat()
        }
        return signJWT(info=info)