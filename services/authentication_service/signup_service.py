from db import User
from sqlalchemy import or_
from cores.databases.connection import get_db
from cores.authen import signJWT, decodeJWT
import datetime
from decouple import config
from services.utils_service.email_service import EmailService
from services.authentication_service.token_service import TokenService
from cores.schemas.sche_base import DataResponse
from utils import util_funcs

class SignUpService():
    def __init__(self, info=None):
        self.session = next(get_db())
        self.info = info

    def verify_signup_info(self):
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
            user = User(
                username=self.info.username,
                email=self.info.email,
                full_name=self.info.full_name,
                phone=self.info.phone,
                # dob=self.info.dob,
                # gender=self.info.gender,
                password=self.info.password
            )
            self.session.add(user)
            self.session.commit()
            self.session.refresh(user)
            return user
        except Exception as e:
            print(e)
            return None
    
    def generate_confirm_token(self, id):
        expires_at = util_funcs.create_expires_duration(seconds=config('SIGNUP_CONFIRM_DURATION'))
        info = util_funcs.token_signup_format(id=id, expires_at=expires_at)
        return signJWT(info=info)
    
    def send_confirm_email(self, token, recipients=None):
        try:
            current_time = datetime.datetime.now()
            expires_duration = config('SIGNUP_CONFIRM_DURATION')
            email_service = EmailService()
            if self.info:
                recipients = [self.info.email]

            email_service.send_mail(
                send_to=recipients,
                title=f'Welcome {current_time} to The Social Hub',
                message=f'''
                    Hello there!
                    Thank you for joining us. Please follow this link to verify your account: {config('FE_VERIFY_URL')}={token}
                    The confirmation link will be expired after {int(expires_duration)/60} minutes
                    Hope you will have a great time with us ^^
                    TheSocialHub Team.
                ''',
            )
            return True
        except Exception as e:
            print(e)
            return False
        
    def verify_user_account(self, token):
        info = decodeJWT(token=token)
        if not info:
            return DataResponse().custom_response(503, False, 'Invalid token')
        expires_at = info['expires_at'] if 'expires_at' in info.keys() else None
        uid = info['uid'] if 'uid' in info.keys() else None
        if not expires_at or not uid:
            return DataResponse().custom_response(503, False, 'Invalid token')

        now = datetime.datetime.now()
        expires_at = datetime.datetime.strptime(expires_at, '%Y-%m-%dT%H:%M:%S.%f')
        if now > expires_at: 
            return DataResponse().custom_response(504, False, 'Verification link expired')
        elif now < expires_at:
            user = self.session.query(User).filter(User.id == uid).first()
            if user.is_verified == True:
                return DataResponse().custom_response(505, False, 'User already verified. Please login to continue.')
            user.is_verified = True
            user.update_time()
            self.session.commit()
            user_token = TokenService(uid=uid).generate_user_token()
            return DataResponse().success_response('Succeed! Welcome to TheSocialHub', token=user_token)
        return DataResponse().custom_response(500, False, 'Verification Failed')
    
    def get_uid_by(self, email=None, username=None):
        if email:
            user = self.session.query(User).filter(User.email == email).first()
        if username:
            user = self.session.query(User).filter(User.username == username).first()
        return user.id if user else None
        
    def get_email_by_uid(self, uid):
        user = self.session.query(User).get(uid)
        return user.email if user else None

        