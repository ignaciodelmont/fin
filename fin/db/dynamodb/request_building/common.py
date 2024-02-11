from enum import Enum


from ..models.common import BaseDDB


class IndexName(Enum):
    gsi1 = "gsi1"


#
# Put Item
#


def build_request_new_item(item: BaseDDB):
    return {
        "Item": item.__dict__,
    }


#
# Get Item
#


def build_item_key(pk, sk):
    return {
        "Key": {
            "pk": pk,
            "sk": sk,
        },
    }


#
# Query Items
#


def build_request_query_items_by_pk(pk):
    request = {
        "KeyConditionExpression": "pk = :pk",
        "ExpressionAttributeValues": {
            ":pk": pk,
        },
    }

    return request
