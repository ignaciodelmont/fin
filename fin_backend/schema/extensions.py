from strawberry.extensions import SchemaExtension
from fin_backend.db.dynamodb import DDBFinClient


class BadRequestError(RuntimeError):
    pass


def is_server_request(execution_context):
    return bool(execution_context.context.get("request"))


def resolve_user_from_request(db_client: DDBFinClient, execution_context):
    user_email = execution_context.context["request"].get("x-user")
    if not user_email:
        return None
    return db_client.users.get_user(user_email)


def get_user_for_context(db_client, execution_context):
    if is_server_request(execution_context):
        return resolve_user_from_request(db_client, execution_context)


class DynamoDBExtension(SchemaExtension):
    def on_operation(self):
        db_client = DDBFinClient()
        self.execution_context.context["db"] = db_client
        self.execution_context.context["user"] = get_user_for_context(
            db_client, self.execution_context
        )
        yield
