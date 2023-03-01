from abc import ABCMeta, abstractmethod

class SchoolLayerContract:
    __metaclass__ = ABCMeta

    @abstractmethod
    def find(self, db, id):
        pass

    @abstractmethod
    def paginate(self, db):
        pass



