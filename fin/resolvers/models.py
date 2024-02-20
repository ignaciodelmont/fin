from pydantic import BaseModel
from typing import List, Optional


class BaseFinModel(BaseModel):
    id: str
    created_at: str
    modified_at: str


class Label(BaseFinModel):
    name: str
    description: str


class Transaction(BaseFinModel):
    amount: float
    currency: str
    name: str
    description: str
    labels: Optional[List[Label]]


class Income(Transaction):
    pass


class Expense(Transaction):
    pass


class TransactionStats(BaseModel):
    currency: str
    total_in: float
    total_out: float
    balance: float
