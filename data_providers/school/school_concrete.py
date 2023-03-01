from decouple import config
from .layers.school_database_layer import SchoolDatabaseLayer
from .layers.school_es_layer import SchoolEsLayer
class SchoolConcrete():
    def __init__(self):
        self.service = SchoolDatabaseLayer() if config('SCHOOL_DATA_PROVIDER',
                                                       'database') == 'database' else SchoolEsLayer()