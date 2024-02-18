from fin.db.dynamodb import DDBFinClient
from .models import Label
from typing import List


def resolve_add_label(db: DDBFinClient, user, name, description):
    return db.labels.add_label(user, name, description)


def resolve_labels(db: DDBFinClient, user) -> List[Label]:
    return [Label(**label.__dict__) for label in db.labels.list_labels(user)]
