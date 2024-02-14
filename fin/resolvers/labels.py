from fin.db.dynamodb import DDBFinClient


def resolve_add_label(db: DDBFinClient, user, name, description):
    return db.labels.add_label(user, name, description)
