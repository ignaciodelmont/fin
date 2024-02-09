from ..models.users import User
from ..models.transactions import Income, Expense, Currency
from . import common as com
from decimal import Decimal
from fin import utils
from typing import Optional


def _gen_transaction_pk(user: User):
    return f"TRANSACTION#{user.id}"


def _gen_income_sk(timestamp):
    return f"{timestamp}#INCOME"


def _gen_expense_sk(timestamp):
    return f"{timestamp}#EXPENSE"


def build_put_income(
    user: User,
    amount: Decimal,
    currency: Currency,
    name: str,
    description: Optional[str] = None,
):
    now = utils.datetime.now()
    id_ = _gen_income_sk(now)

    return {
        **com.build_request_new_item(
            Income(
                pk=_gen_transaction_pk(user),
                sk=id_,
                user_id=user.id,
                id=id_,
                created_at=now,
                modified_at=now,
                amount=amount,
                currency=currency,
                name=name,
                description=description,
            )
        )
    }


def build_put_expense(
    user: User,
    amount: Decimal,
    currency: Currency,
    name: str,
    description: Optional[str] = None,
):
    now = utils.datetime.now()
    id_ = _gen_expense_sk(now)

    return {
        **com.build_request_new_item(
            Expense(
                pk=_gen_transaction_pk(user),
                sk=id_,
                user_id=user.id,
                id=id_,
                created_at=now,
                modified_at=now,
                amount=amount,
                currency=currency,
                name=name,
                description=description,
            )
        )
    }


def build_query_transactions(user: User):
    return com.build_request_query_items_by_pk(_gen_transaction_pk(user))


def build_delete_transaction(user: User, transaction_id: str):
    return com.build_item_key(_gen_transaction_pk(user), transaction_id)
