from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, SmallInteger, BigInteger, JSON, Text, Boolean
from db import Base
from sqlalchemy.dialects.mysql import BIGINT, TINYINT
from cores.models.base_model import BaseModel
class School(BaseModel):
    __tablename__ = 'school'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(50), nullable=False)
    name = Column(String(255), nullable=False)
    targets = Column(Integer, nullable=False)
    phone = Column(String(20), nullable=True)
    email = Column(String(128), nullable=True)
    avatar = Column(JSON, nullable=True)
    logo = Column(String(255), nullable=True)
    website = Column(String(128), nullable=True)
    description = Column(Text, nullable=True)
    seo_description = Column(Text, nullable=True)
    vision = Column(Text, nullable=True)
    mission = Column(Text, nullable=True)
    enrollment_targets = Column(Integer)
    method_content = Column(Text, nullable=True)
    is_outstanding = Column(Boolean, default=0)
    order = Column(Integer, nullable=True)
    # view = Column(BIGINT, default=0)
    state = Column(String(20), default='PENDING')
