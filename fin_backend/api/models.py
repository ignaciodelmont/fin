from pydantic import BaseModel
from enum import Enum
from typing import Optional
from decimal import Decimal


class Currency(Enum):
    ARS = "ARS"
    USD = "USD"


class NewTransactionDTO(BaseModel):
    name: str
    amount: Decimal
    description: Optional[str]
    currency: Currency


class RemoveTransactionDTO(BaseModel):
    id: str
