from sqlalchemy import Column, Integer, String, BigInteger, UUID
from db.db_connector import Base
import uuid


class QuoteTable(Base):
    __tablename__ = 'quotes'
    __table_args__ = {'schema': 'mq'}

    id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True)
    quote_id = Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4, nullable=False)
    author = Column(String(255))
    category = Column(String(255))
    image_url = Column(String(255), nullable=False)
    like_count = Column(BigInteger, default=0)
    share_count = Column(BigInteger, default=0)
