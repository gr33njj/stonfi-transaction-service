from sqlalchemy import Column, Integer, String, Float, DateTime
from app.database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    wallet_address = Column(String, index=True)
    transaction_hash = Column(String, unique=True, index=True)
    pool_address = Column(String)
    amount_in = Column(Float)
    amount_out = Column(Float)
    token_in = Column(String)
    token_out = Column(String)
    timestamp = Column(DateTime)
    status = Column(String)
