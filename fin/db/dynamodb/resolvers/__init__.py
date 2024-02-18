from decimal import Decimal
from fin.db.dynamodb.request_building import users as users_rb
from fin.db.dynamodb.request_building import transactions as transactions_rb
from fin.db.dynamodb.request_building import labels as labels_rb
from ..models.users import User
from ..models.transactions import Currency, Income, Expense, Transaction
from ..models.labels import Label
from typing import Optional, List


class UsersResolvers:
    def __init__(self, client):
        self.client = client

    def add_user(self, name: str, username: str, email: str) -> User:
        request = users_rb.build_put_user(username, email, name)
        response = self.client.put_item(request)
        return User(**response)

    def get_user(self, email: str) -> User:
        request = users_rb.build_get_user(email)
        response = self.client.get_item(request)
        return User(**response) if response else response


class TransactionsResolvers:
    def __init__(self, client):
        self.client = client

    def add_income(
        self,
        user: User,
        amount: Decimal,
        currency: Currency,
        name: str,
        description: Optional[str] = None,
        label_ids: Optional[List[str]] = None,
    ) -> Income:
        request = transactions_rb.build_put_income(
            user, amount, currency, name, description, label_ids
        )
        response = self.client.put_item(request)
        return Income(**response)

    def add_expense(
        self,
        user: User,
        amount: Decimal,
        currency: Currency,
        name: str,
        description: Optional[str] = None,
        label_ids: Optional[List[str]] = None,
    ) -> Expense:
        request = transactions_rb.build_put_expense(
            user, amount, currency, name, description, label_ids
        )
        response = self.client.put_item(request)
        return Expense(**response)

    def list_transactions(self, user: User) -> List[Transaction]:
        request = transactions_rb.build_query_transactions(user)
        response = self.client.query(request)

        def is_income(item):
            return "income" in item["sk"].lower()

        return [
            Income(**item) if is_income(item) else Expense(**item) for item in response
        ]

    def delete_transaction(self, user: User, transaction_id: str):
        request = transactions_rb.build_delete_transaction(user, transaction_id)
        self.client.delete_item(request)


class LabelsResolvers:
    def __init__(self, client):
        self.client = client

    def add_label(self, user: User, name: str, description: Optional[str] = None):
        request = labels_rb.build_put_label(user, name, description)
        return Label(**self.client.put_item(request))

    def list_labels(self, user: User):
        request = labels_rb.build_query_labels(user)
        response = self.client.query(request)
        return [Label(**item) for item in response]

    def delete_label(self, user: User, label_id: str):
        pass
