from fin import utils
from ..request_building import common as com
from ..models.labels import Label


def _gen_pk_label(user):
    return f"LABEL#{user.id}"


def _gen_sk_label():
    return utils.ids.generate_uuid()


def build_put_label(user, name, description):
    now = utils.datetime.now()
    sk = _gen_sk_label()
    return com.build_request_new_item(
        Label(
            pk=_gen_pk_label(user),
            sk=sk,
            id=sk,
            created_at=now,
            modified_at=now,
            name=name,
            description=description,
        )
    )


def build_query_labels(user):
    return com.build_request_query_items_by_pk(_gen_pk_label(user))
