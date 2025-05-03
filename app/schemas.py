from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TransactionBase(BaseModel):
    wallet_address: str
    transaction_hash: str
    pool_address: str
    amount_in: float
    amount_out: float
    token_in: str
    token_out: str
    timestamp: datetime
    status: str

class TransactionCreate(TransactionBase):
    pass

class TransactionResponse(TransactionBase):
    id: int

    class Config:
        from_attributes = True

class TransactionFilter(BaseModel):
    wallet_address: str
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

class WalletAddress(BaseModel):
    wallet_address: str