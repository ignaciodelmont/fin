from fin_backend.db.dynamodb import DDBFinClient


def resolve_add_income(db: DDBFinClient, user, amount, currency, name, description):
    return db.transactions.add_income(user, amount, currency, name, description)


def resolve_add_expense(db: DDBFinClient, user, amount, currency, name, description):
    return db.transactions.add_expense(user, amount, currency, name, description)


def resolve_transactions(db: DDBFinClient, user):
    return db.transactions.list_transactions(user)


def resolve_delete_transaction(db: DDBFinClient, user, transaction_id):
    return db.transactions.delete_transaction(user, transaction_id)
