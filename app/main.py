from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal, Base, engine
from app.models import Transaction
from app.schemas import TransactionCreate, TransactionResponse, TransactionFilter, WalletAddress
from app.tonapi_client import TonAPIClient
from typing import List

app = FastAPI(title="Сервис транзакций STON.fi")

Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "Добро пожаловать в сервис транзакций STON.fi! Доступные эндпоинты: POST /transactions/fetch, POST /transactions/filter. Документация: /docs"}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/transactions/fetch", response_model=List[TransactionResponse])
async def fetch_transactions(wallet: WalletAddress, db: Session = Depends(get_db)):
    client = TonAPIClient()
    transactions = await client.get_swap_transactions(wallet.wallet_address)
    
    if not transactions:
        raise HTTPException(status_code=404, detail="Транзакции обмена не найдены")
    
    saved_transactions = []
    for tx in transactions:
        existing_tx = db.query(Transaction).filter(Transaction.transaction_hash == tx["transaction_hash"]).first()
        if not existing_tx:
            db_tx = Transaction(**tx)
            db.add(db_tx)
            db.commit()
            db.refresh(db_tx)
            saved_transactions.append(db_tx)
    
    return saved_transactions

@app.post("/transactions/filter", response_model=List[TransactionResponse])
async def filter_transactions(filter: TransactionFilter, db: Session = Depends(get_db)):
    query = db.query(Transaction).filter(Transaction.wallet_address == filter.wallet_address)
    
    if filter.start_time:
        query = query.filter(Transaction.timestamp >= filter.start_time)
    if filter.end_time:
        query = query.filter(Transaction.timestamp <= filter.end_time)
    
    transactions = query.all()
    
    if not transactions:
        raise HTTPException(status_code=404, detail="Транзакции по указанным фильтрам не найдены")
    
    return transactions