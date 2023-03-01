from repositories.services.school_address_service import SchoolAddressService
from .school_address_layer_contract import SchoolAddressLayerContract
class SchoolAddressDatabaseLayer(SchoolAddressLayerContract):
    def find(self, db, id):
        return SchoolAddressService().repo.find(db, id)