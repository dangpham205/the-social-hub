from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

# from cores.databases.connection import Connection
# from cores.databases.database import Database
# from cores.databases.db_helper import DBHelper

"""
    Import các class cần cho việc tạo bảng. Import class nào thì tạo bảng đó
"""
from .models.school import School
from .models.address import Address
from .models.infrastructure import Infrastructer
from .models.enrollment_information import EnrollmentInformation
from .models.staff import Staff
from .models.category import Category
from .models.post import Post
from .models.news import News
from .models.link import Link
from cores.activity_logs.activity_log_model import ActivityLog

