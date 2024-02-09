from enum import Enum


from ..models.common import BaseDDB


class ConditionOperator(Enum):
    AND = "AND"
    OR = "OR"


class IndexName(Enum):
    gsi1 = "gsi1"


_ID_SPLITTER = "#_#"


def id_from_pk_sk(pk, sk):
    return f"{pk}{_ID_SPLITTER}{sk}"


def pk_sk_from_id(id):
    pk, sk = id.split(_ID_SPLITTER)
    return pk, sk


def map_raw_item(raw_item):
    return {
        "id": (
            id_from_pk_sk(raw_item["pk"], raw_item["sk"])
            if "id" not in raw_item
            else raw_item["id"]
        ),
        **raw_item,
    }


def build_request_new_item(item: BaseDDB):
    return {
        "Item": item.__dict__,
    }


def add_conditional_expression(
    request: dict,
    expression: str,
    expression_attribute_values: dict,
    conditional_operator: ConditionOperator,
):
    if "ConditionExpression" in request:
        cond_expression = f"({request['ConditionExpression']}) {conditional_operator.value} {expression}"
    else:
        cond_expression = expression

    return {
        **request,
        "ConditionExpression": cond_expression,
        "ExpressionAttributeValues": {
            **request.get("ExpressionAttributeValues", {}),
            **expression_attribute_values,
        },
    }


def build_item_key(pk, sk):
    return {
        "Key": {
            "pk": pk,
            "sk": sk,
        },
    }


def build_request_query_items_by_pk(pk):
    request = {
        "KeyConditionExpression": "pk = :pk",
        "ExpressionAttributeValues": {
            ":pk": pk,
        },
    }

    return request
