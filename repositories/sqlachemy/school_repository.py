from cores.repositories.abstracts.sqlachemy_abstract import SqlAchemyAbstract
from db import School
from sqlalchemy.orm import Session
from repositories.contracts.school_contract import SchoolContract
class SchoolRepository(SqlAchemyAbstract, SchoolContract):
    def __init__(self):
        self.set_model(School)
        super().__init__()

    def get_by(self, db, user_id):
        return user_id
