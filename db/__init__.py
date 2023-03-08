from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

# from cores.databases.connection import Connection
# from cores.databases.database import Database
# from cores.databases.db_helper import DBHelper

"""
    Import các class cần cho việc tạo bảng. Import class nào thì tạo bảng đó
"""
from .models.user import User
# from .models.like import Like
from .models.post import Post

