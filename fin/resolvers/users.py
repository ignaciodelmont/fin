from fin.db.dynamodb import DDBFinClient


def resolve_add_user(db: DDBFinClient, name: str, email: str, username: str):
    return db.users.add_user(name, username, email)


def resolve_get_user(db: DDBFinClient, email: str):
    return db.users.get_user(email)
