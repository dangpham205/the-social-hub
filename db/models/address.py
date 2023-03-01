from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, SmallInteger, BigInteger, JSON, Text, Boolean
from db import Base
from sqlalchemy.dialects.mysql import BIGINT, TINYINT
from cores.models.base_model import BaseModel


class Address(BaseModel):
    __incomplete_tablename__ = 'address'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }

    id = Column(Integer, primary_key=True, autoincrement=True)
    school_id = Column(Integer, ForeignKey('school.id'))
    address = Column(Text, nullable=False)
    province_id = Column(Integer, nullable=False)
    district_id = Column(Integer, nullable=True)
    ward_id = Column(Integer, nullable=True)
    phone = Column(String(20), nullable=True)
    is_default = Column(Boolean)
    school = relationship('School', backref='addresses', 
                          primaryjoin="and_(School.id==Address.school_id, School.deleted_at == None)")
