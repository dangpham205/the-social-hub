from decouple import config
from .layers.school_address_database_layer import SchoolAddressDatabaseLayer
from .layers.school_address_es_layer import SchoolAddressEsLayer
class SchoolAddressConcrete():
    def __init__(self):
        self.service = SchoolAddressDatabaseLayer() if config('SCHOOL_DATA_PROVIDER',
                                                       'database') == 'database' else SchoolAddressEsLayer()