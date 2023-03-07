from services.authentication_service import TokenService
from cores.databases.connection import get_db
from db import Post
from cores.schemas.sche_base import DataResponse

class PostService():
    def __init__(self, user_token: str):
        self.user_token = user_token
        self.session = next(get_db())
        self.uid = None
        self.__get_uid()

    def __get_uid(self):
        token_service = TokenService(token=self.user_token)
        uid = token_service.get_uid_from_token()
        if uid:
            self.uid = uid

    def create_post(self):
        pass