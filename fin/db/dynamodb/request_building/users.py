from ..request_building import common as com
from fin.utils import datetime as dt, ids
from ..models import users


def _gen_pk_user():
    return "USER"


def _gen_sk_user(email):
    return email


def _gen_id_user():
    return ids.generate_uuid()


def build_put_user(username, email, name):
    # TODO: Prevent duplicate usernames and emails
    created_at = dt.now()
    return {
        **com.build_request_new_item(
            users.User(
                pk=_gen_pk_user(),
                sk=_gen_sk_user(email),
                id=_gen_id_user(),
                username=username,
                email=email,
                name=name,
                created_at=created_at,
                modified_at=created_at,
            )
        ),
        "ConditionExpression": "attribute_not_exists(sk)",
    }


def build_get_user(email):
    return com.build_item_key(_gen_pk_user(), _gen_sk_user(email))
