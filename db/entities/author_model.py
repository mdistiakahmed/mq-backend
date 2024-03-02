from sqlalchemy import Column, String, BigInteger
from db.db_connector import Base


class AuthorTable(Base):
    __tablename__ = 'author'
    __table_args__ = {'schema': 'mq'}

    id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(255))
