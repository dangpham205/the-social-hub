from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from db import Base
from cores.models.base_model import BaseModel


class Link(BaseModel):
    __incomplete_tablename__ = 'link'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }

    id = Column(Integer, primary_key=True, autoincrement=True)
    school_id = Column(Integer, ForeignKey('school.id'))
    link = Column(String(400), nullable=False)
    thumb = Column(String(400), nullable=False)
    title = Column(String(400), nullable=False)
    type = Column(Enum('NEWS', 'MEGASTORY'), nullable=False)
    school = relationship('School', backref='link', 
                          primaryjoin="and_(School.id==Link.school_id, School.deleted_at == None)")
