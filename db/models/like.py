from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, SmallInteger, BigInteger, JSON, Text, Boolean
from db import Base
from sqlalchemy.dialects.mysql import BIGINT, TINYINT
from cores.models.base_model import BaseModel
from enums.db import model_enum, table_name_enum


class Like(BaseModel):
    __tablename__ = table_name_enum.LIKE
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    post_id = Column(Integer, ForeignKey('post.id'))
    content = Column(Boolean, nullable=True)
    user = relationship('User', backref='user', 
                          primaryjoin="and_(User.id==Like.user_id, User.deleted_at == None)")
    post = relationship('Post', backref='post', 
                          primaryjoin="and_(Post.id==Like.post_id, Post.deleted_at == None)")
    
