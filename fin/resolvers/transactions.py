from fin.db.dynamodb import DDBFinClient
from typing import List
from ..resolvers import labels as rlabels
from .models import Transaction, Income, Expense, TransactionStats


def resolve_add_income(
    db: DDBFinClient, user, amount, currency, name, description, label_ids
):
    return db.transactions.add_income(
        user, amount, currency, name, description, label_ids
    )


def resolve_add_expense(
    db: DDBFinClient, user, amount, currency, name, description, label_ids
):
    return db.transactions.add_expense(
        user, amount, currency, name, description, label_ids
    )


def _map_transaction(transaction_from_db, labels_by_id) -> Transaction:
    t_type = (
        Income
        if transaction_from_db.__class__.__name__.lower() == "income"
        else Expense
    )

    transaction = t_type(
        **transaction_from_db.__dict__,
        labels=[labels_by_id[l_id] for l_id in (transaction_from_db.label_ids or [])]
    )

    return transaction


def resolve_transactions(db: DDBFinClient, user) -> List[Transaction]:
    transactions = db.transactions.list_transactions(user)
    labels = rlabels.resolve_labels(db, user)
    labels_by_id = {label.id: label for label in labels}

    return [_map_transaction(transaction, labels_by_id) for transaction in transactions]


def compute_transaction_stats(
    transactions: List[Transaction],
) -> List[TransactionStats]:
    def _group_by_currency(transactions: List[Transaction]) -> dict:
        grouped = {}
        for t in transactions:
            grouped[t.currency] = grouped.get(t.currency, []) + [t]

        return grouped

    def _compute_transaction_stats(
        currency: str, transactions: List[Transaction]
    ) -> TransactionStats:
        total_income = sum([t.amount for t in transactions if isinstance(t, Income)])
        total_expense = sum([t.amount for t in transactions if isinstance(t, Expense)])
        balance = total_income - total_expense
        return TransactionStats(
            currency=currency,
            balance=balance,
            total_in=total_income,
            total_out=total_expense,
        )

    return map(
        lambda kv: _compute_transaction_stats(*kv),
        _group_by_currency(transactions).items(),
    )


def resolve_delete_transaction(db: DDBFinClient, user, transaction_id):
    return db.transactions.delete_transaction(user, transaction_id)
