from ..models.users import User
from ..models.transactions import Income, Expense, Currency
from . import common as com
from decimal import Decimal
from fin import utils
from typing import Optional, List


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
    label_ids: Optional[List[str]] = None,
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
                label_ids=label_ids,
            )
        )
    }


def build_put_expense(
    user: User,
    amount: Decimal,
    currency: Currency,
    name: str,
    description: Optional[str] = None,
    label_ids: Optional[List[str]] = None,
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
                label_ids=label_ids,
            )
        )
    }


def build_query_transactions(user: User, filters):
    base_req = com.build_request_query_items_by_pk(_gen_transaction_pk(user))
    start_date = filters.start_date
    end_date = filters.end_date

    if start_date and end_date:
        condition_expression = com.between("sk", ":sk_start", ":sk_end")
        expression_attribute_values = {":sk_start": start_date, ":sk_end": end_date}
    elif start_date:
        condition_expression = com.gte("sk", ":sk_start")
        expression_attribute_values = {":sk_start": start_date}
    elif end_date:
        condition_expression = com.lt("sk", ":sk_end")
        expression_attribute_values = {":sk_end": end_date}
    else:
        condition_expression = None
        expression_attribute_values = None

    return com.add_expression_attribute_values(
        com.add_key_condition_expression(base_req, condition_expression),
        expression_attribute_values,
    )


def build_delete_transaction(user: User, transaction_id: str):
    return com.build_item_key(_gen_transaction_pk(user), transaction_id)
