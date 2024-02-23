from enum import Enum


from ..models.common import BaseDDB


class IndexName(Enum):
    gsi1 = "gsi1"


#
# Utils
#


def parenthesize(expression):
    return f"({expression})"


#
# Fitering
#


def and_(*args):
    return (
        " AND ".join(parenthesize(arg) for arg in args if arg)
        if len(args) > 1
        else args
    )


def or_(*args):
    return (
        " OR ".join(parenthesize(arg) for arg in args if arg) if len(args) > 1 else args
    )


def gte(attr, value):
    return f"{attr} >= {value}"


def lt(attr, value):
    return f"{attr} < {value}"


def lte(attr, value):
    return f"{attr} <= {value}"


def between(attr, value1, value2):
    return f"{attr} BETWEEN {value1} AND {value2}"


def add_key_condition_expression(base_req, condition):
    if not condition:
        return base_req

    new_key_condition_expression = and_(
        base_req.get("KeyConditionExpression", ""), condition
    )
    return {
        **base_req,
        "KeyConditionExpression": new_key_condition_expression,
    }


def add_expression_attribute_values(base_req, values):
    if not values:
        return base_req

    return {
        **base_req,
        "ExpressionAttributeValues": {
            **base_req.get("ExpressionAttributeValues", {}),
            **values,
        },
    }


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
