import sqlalchemy as sa
import datetime


class BaseMixin(object):
    __table_args__ = {'mysql_engine': 'InnoDB'}

    created_at = sa.Column('created_at', sa.Integer, nullable=False)
    updated_at = sa.Column('updated_at', sa.Integer, nullable=False)

    @staticmethod
    def create_time(mapper, connection, instance):
        now = datetime.datetime.now()
        instance.created_at = now.timestamp()
        instance.updated_at = now.timestamp()

    @staticmethod
    def update_time(mapper, connection, instance):
        now = datetime.datetime.now()
        instance.updated_at = now.timestamp()


    @classmethod
    def register(cls):
        sa.event.listen(cls, 'before_insert', cls.create_time)
        sa.event.listen(cls, 'before_update', cls.update_time)
