from sqlalchemy import Column, Integer, String

from db.db_connector import Base


class UserTable(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'mq'}

    id = Column('id', Integer, primary_key=True, nullable=False, autoincrement=True)
    username = Column(String)
    user_status = Column(String)
