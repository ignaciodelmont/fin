from fin import utils
from ..request_building import common as com
from ..models.labels import Label


def _gen_pk_label(user):
    return f"LABEL#{user.id}"


def _gen_sk_label():
    return utils.ids.generate_uuid()


def build_put_label(user, name, description):
    now = utils.datetime.now()

    return com.build_request_new_item(
        Label(
            pk=_gen_pk_label(user),
            sk=_gen_sk_label(),
            created_at=now,
            modified_at=now,
            name=name,
            description=description
        )
    )
