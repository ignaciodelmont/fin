from dataclasses import dataclass
from .common import BaseDDB
from decimal import Decimal
from enum import Enum
from typing import Optional


class Currency(Enum):
    USD = "USD"
    EUR = "EUR"
    ARS = "ARS"


@dataclass
class Transaction(BaseDDB):
    id: str
    user_id: str
    amount: Decimal
    currency: Currency
    name: str
    description: Optional[str] = None

    def transaction_type(self):
        print("sk", self.sk)
        return self.sk.split("#")[0]


@dataclass
class Income(Transaction):
    pass


class Expense(Transaction):
    pass
