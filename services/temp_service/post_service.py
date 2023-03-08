from services.authentication_service import TokenService
from cores.databases.connection import get_db
from db import Post
from cores.schemas.sche_base import DataResponse
from v1.schemas import post_schema
from sqlalchemy import and_, desc, or_

class PostService():
    def __init__(self, user_token: str):
        self.session = next(get_db())
        self.user_token = user_token
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
        
    def delete_post(self, id):
        post = self.session.query(Post).filter(Post.id == id, Post.deleted_at == None).first()
        if not post:
            return DataResponse().custom_response(500, False, "Post not found")
        
        if post.user_id != self.uid:
            return DataResponse().custom_response(405, False, "What à dú đo ình")
        
        post.delete()
        self.session.commit()
        return DataResponse().success_response('Delete post succeed')
    
    def paginate_posts(self):
        data = self.session.query(Post).filter(Post.deleted_at ==None).order_by(desc(Post.updated_at)).all()
        return DataResponse().success_response(data=data)
        