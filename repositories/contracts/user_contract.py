from abc import ABCMeta, abstractmethod
from cores.repositories.contracts.repository_contract import SqlAchemyContracts
class UserContract(SqlAchemyContracts):
    __metaclass__ = ABCMeta
    
    def __init__(self):
        print('user contract')
    
    @abstractmethod
    def get_by(self, db, user_id):
        pass

