from abc import ABCMeta, abstractmethod
from cores.repositories.contracts.repository_contract import SqlAchemyContracts
class SchoolContract(SqlAchemyContracts):
    __metaclass__ = ABCMeta
    @abstractmethod
    def get_by(self, db, user_id):
        pass

    def import_data(self, db, school_id, file):
        pass

    def export_data(self, db, school_id):
        pass
