from db import User
from cores.databases.connection import get_db


class LoginService():
    def __init__(self, info=None):
        self.session = next(get_db())
        self.info = info

    def get_uid(self):
        if '@' in self.info.user:
            user = self.session.query(User).filter(User.email == self.info.user).first()
        else:
            user = self.session.query(User).filter(User.username == self.info.user).first()
        return user.id if user else None
    
    def check_user_verified(self, uid):
        user = self.session.query(User).get(uid)
        return user.is_verified
        
    def verify_password(self, uid):
        user = self.session.query(User).filter(User.id == uid).first()
        return user.check_password(self.info.password)