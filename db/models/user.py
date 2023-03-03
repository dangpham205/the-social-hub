from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, SmallInteger, BigInteger, JSON, Text, Boolean, Enum
from db import Base
from sqlalchemy.dialects.mysql import BIGINT, TINYINT
from cores.models.base_model import BaseModel
from enums.db import model_enum, table_name_enum

class User(BaseModel):
    __tablename__ = table_name_enum.USER
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
    }

    username = Column(String(25), nullable=False, index = True, unique = True)
    email = Column(String(100), nullable=False, index = True, unique = True)
    full_name = Column(String(100), nullable=False)
    phone = Column(String(15), nullable=True)
    avatar = Column(String(300), nullable=True)
    avatar_2nd = Column(String(300), nullable=True)
    bio = Column(String(300), nullable=True)
    dob = Column(DateTime, nullable=False)
    gender = Column(Enum(model_enum.GenderEnum), nullable=False)
    location = Column(String(300), nullable=True)
    is_verified = Column(Boolean, nullable=False, default=False)
