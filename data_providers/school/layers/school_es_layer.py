from repositories.services.school_service import SchoolService
from .school_layer_contract import SchoolLayerContract
class SchoolEsLayer(SchoolLayerContract):
    def find(self, db, id):
        return SchoolService().repo.find(db, id)