from sqlalchemy import Column, String, BigInteger
from db.db_connector import Base


class CategoryTable(Base):
    __tablename__ = 'category'
    __table_args__ = {'schema': 'mq'}

    id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(255))
