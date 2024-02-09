import strawberry as st
from enum import Enum
from typing import List, Optional
import decimal
import datetime
from fin_backend.schema.extensions import DynamoDBExtension
from fin_backend.resolvers import users as users_resolvers
from fin_backend.resolvers import transactions as transactions_resolvers
from fin_backend.utils import mapping as mp
from .scalars import DateTimeCustom

#
# Transactions
#


@st.enum
class Currency(Enum):
    USD = "USD"
    EUR = "EUR"
    ARS = "ARS"


@st.interface
class Transaction:
    id: st.ID
    amount: decimal.Decimal
    created_at: DateTimeCustom
    modified_at: DateTimeCustom
    currency: Currency
    name: str
    description: Optional[str]


@st.type
class Income(Transaction):
    pass


@st.type
class Expense(Transaction):
    pass


#
# Users
#


@st.type
class User:
    id: st.ID
    name: str
    username: str
    email: str
    created_at: DateTimeCustom
    modified_at: DateTimeCustom


@st.type
class Query:
    @st.field
    def user(self, root, info, email: str) -> User:
        user = users_resolvers.resolve_get_user(info.context["db"], email)
        return mp.map_res_with_type(User, user)

    @st.field
    def transactions(self, root, info) -> List[Transaction]:
        user = info.context["user"]
        transactions = transactions_resolvers.resolve_transactions(
            info.context["db"], user
        )
        print("Transactions", transactions)
        return [
            mp.map_res_with_type(
                Income if t.transaction_type() == "income" else Expense, t
            )
            for t in transactions
        ]


@st.type
class Mutation:
    @st.mutation
    def add_user(self, root, info, name: str, username: str, email: str) -> User:
        new_user = users_resolvers.resolve_add_user(
            info.context["db"], name, email, username
        )
        return mp.map_res_with_type(User, new_user)

    @st.mutation
    def add_income(
        self,
        root,
        info,
        amount: decimal.Decimal,
        currency: Currency,
        name: str,
        description: Optional[str] = None,
    ) -> Income:
        user = info.context["user"]
        new_income = transactions_resolvers.resolve_add_income(
            info.context["db"], user, amount, currency, name, description
        )
        return mp.map_res_with_type(Income, new_income)

    @st.mutation
    def add_expense(
        self,
        root,
        info,
        amount: decimal.Decimal,
        currency: Currency,
        name: str,
        description: Optional[str] = None,
    ) -> Income:
        user = info.context["user"]
        new_expense = transactions_resolvers.resolve_add_expense(
            info.context["db"], user, amount, currency, name, description
        )
        return mp.map_res_with_type(Expense, new_expense)


schema = st.Schema(
    query=Query,
    mutation=Mutation,
    types=[Income, Expense],
    extensions=[DynamoDBExtension],
)
