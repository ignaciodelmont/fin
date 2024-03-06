import fin.db.dynamodb.request_building.common as common
from fin.db.dynamodb.models.common import BaseDDB
from dataclasses import dataclass


@dataclass
class TestDynamoDBModel(BaseDDB):
    name: str
    age: int


def test_build_request_new_item():
    obj = TestDynamoDBModel(
        pk="pk",
        sk="sk",
        name="name",
        age=26,
        created_at="2024-01-01",
        modified_at="2024-01-01",
    )

    assert common.build_request_new_item(obj) == {
        "Item": {
            "pk": "pk",
            "sk": "sk",
            "name": "name",
            "age": 26,
            "created_at": "2024-01-01",
            "modified_at": "2024-01-01",
        },
    }


def test_build_item_key():
    assert common.build_item_key(
        "<pk>",
        "<sk>",
    ) == {
        "Key": {
            "pk": "<pk>",
            "sk": "<sk>",
        },
    }


def test_build_request_queri_items_by_pk():
    assert common.build_request_query_items_by_pk(
        "<pk>",
    ) == {
        "KeyConditionExpression": "pk = :pk",
        "ExpressionAttributeValues": {
            ":pk": "<pk>",
        },
    }
