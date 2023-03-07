from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, SmallInteger, BigInteger, JSON, Text, Boolean, Enum
from db import Base
from sqlalchemy.dialects.mysql import BIGINT, TINYINT
from cores.models.base_model import BaseModel
from enums.db import model_enum, table_name_enum
import hashlib

class User(BaseModel):
    __tablename__ = table_name_enum.USER
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
    }

    username = Column(String(25), nullable=False, index = True, unique = True)
    email = Column(String(100), nullable=False, index = True, unique = True)
    full_name = Column(String(100), nullable=False)
    password_hash = Column(String(100), nullable=False)
    phone = Column(String(15), nullable=True)
    avatar = Column(String(300), nullable=True)
    avatar_2nd = Column(String(300), nullable=True)
    bio = Column(String(300), nullable=True)
    dob = Column(DateTime, nullable=True)
    gender = Column(Enum(model_enum.GenderEnum), nullable=True)
    location = Column(String(300), nullable=True)
    is_verified = Column(Boolean, nullable=False, default=False)

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = hashlib.sha256(plain_text_password.encode()).hexdigest()

    def check_password(self, attempted_password):
        return hashlib.sha256(attempted_password.encode()).hexdigest() == self.password_hash
    
    
    def __repr__(self) -> str:
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'avatar': self.avatar,
            'avatar_2nd': self.avatar_2nd,
            'bio': self.bio,
            'dob': self.dob,
            'gender': self.gender,
            'location': self.location,
        }