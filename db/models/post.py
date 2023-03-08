from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, SmallInteger, BigInteger, JSON, Text, Boolean
from db import Base
from sqlalchemy.dialects.mysql import BIGINT, TINYINT
from cores.models.base_model import BaseModel
from enums.db import model_enum, table_name_enum


class Post(BaseModel):
    __tablename__ = table_name_enum.POST
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    content = Column(Text, nullable=False)
    picture = Column(String(20), nullable=True)
    user = relationship('User', backref='posts', 
                          primaryjoin="and_(User.id==Post.user_id, User.deleted_at == None)")
    
    
    def __repr__(self) -> str:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'content': self.content,
            'picture': self.picture,
        }
    
