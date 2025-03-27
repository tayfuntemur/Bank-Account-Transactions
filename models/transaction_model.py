# models/transaction_model.py

from dataclasses import dataclass
from datetime import datetime

@dataclass
class Transaction:
    transactions_id: int
    account_id: int
    amount: float
    transactions_type: str
    kategori: str
    descriptions: str
    transactions_date: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
