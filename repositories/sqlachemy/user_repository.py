from cores.repositories.abstracts.sqlachemy_abstract import SqlAchemyAbstract
from db import User
from sqlalchemy.orm import Session
from repositories.contracts.user_contract import UserContract
class UserRepository(SqlAchemyAbstract, UserContract):
    def __init__(self):
        self.set_model(User)
        super().__init__()

    def get_by(self, db, user_id):
        return user_id
