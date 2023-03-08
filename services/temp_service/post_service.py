from services.authentication_service import TokenService
from cores.databases.connection import get_db
from db.models.post import Post
from cores.schemas.sche_base import DataResponse
from v1.schemas import post_schema

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

    def create_post(self, post: post_schema.CreatePostSchema):
        if self.uid != post.user_id:
            return DataResponse().custom_response(405, False, "What à dú đo ình")
        try:
            new_post = Post(**post.dict())
            self.session.add(new_post)
            self.session.commit()
            return DataResponse().success_response('Create new post succeed')
        except Exception:
            return DataResponse().custom_response(500, False, 'Create new post failed. Please try again later.')