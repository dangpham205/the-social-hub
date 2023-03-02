from abc import ABCMeta, abstractmethod
from sqlalchemy.orm import Session
class SqlAchemyContracts:
    __metaclass__ = ABCMeta
    @abstractmethod
    def find(self, db: Session, id: int, with_trash: bool = False):
        pass

    @abstractmethod
    def get_by_user_id(self, db: Session, user_id, is_get_first: bool = True, is_primary: bool = False, with_trash: bool = False, order='asc'):
        pass

    @abstractmethod
    def search(self, db: Session, fields: dict = [], is_absolute: bool = False, is_get_first: bool = True):
        pass

    @abstractmethod
    def get_all(self, db: Session, with_trash: bool = False):
        pass

    @abstractmethod
    def get_all_with_trash(self, db: Session):
        pass

    @abstractmethod
    def paginate(self, db: Session, params_pagination, params=None, with_trash: bool = False):
        pass

    @abstractmethod
    def paginate_with_trash(self, db: Session, params):
        pass

    @abstractmethod
    def create(self, db: Session, obj):
        pass

    @abstractmethod
    def update(self, db: Session, id, obj, with_restore: bool = False):
        pass

    @abstractmethod
    def delete(self, db: Session, id, is_hard_delete: bool = False):
        pass
