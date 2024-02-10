import pytest
from fin import utils as fb_utils
import datetime as dt
from fin import db
from fin import configs
from fin.schema import extensions
from tests.schema import utils


@pytest.fixture(autouse=True)
def monkeypatch_now(monkeypatch):
    def deterministic_now():
        accumulated_minutes = 0

        def generator():
            nonlocal accumulated_minutes
            while True:
                accumulated_minutes += 1
                yield (
                    dt.datetime(2024, 1, 1) + dt.timedelta(minutes=accumulated_minutes)
                ).isoformat(timespec="milliseconds")

        return generator()

    now_generator = deterministic_now()

    monkeypatch.setattr(fb_utils.datetime, "now", lambda: next(now_generator))


@pytest.fixture(autouse=True)
def monkeypatch_generate_uuid(monkeypatch):
    def deterministic_uuid():
        accumulated_ids = 0

        def generator():
            nonlocal accumulated_ids

            while True:
                accumulated_ids += 1
                yield f"deterministic-id-{accumulated_ids}"

        return generator()

    uuid_generator = deterministic_uuid()

    monkeypatch.setattr(fb_utils.ids, "generate_uuid", lambda: next(uuid_generator))


@pytest.fixture(autouse=True)
def wipe_dynamodb_table():
    """
    Scans the entire db and wipes it out after every test.
    """
    yield
    client = db.dynamodb.DDBFinClient()
    all_items = client.client.scan()
    with client.client.batch_writer() as batch:
        for item in all_items:
            batch.delete_item(Key={"pk": item["pk"], "sk": item["sk"]})


@pytest.fixture
def monkeypatch_dynamodb_extension(monkeypatch):
    db_client = db.dynamodb.DDBFinClient()
    test_user = db_client.users.add_user("Test User", "testuser", "test@user.com")

    def on_operation(self):
        self.execution_context.context["db"] = db_client
        self.execution_context.context["user"] = test_user
        yield

    monkeypatch.setattr(extensions.DynamoDBExtension, "on_operation", on_operation)
    yield


@pytest.fixture
def execute(monkeypatch_dynamodb_extension):
    yield utils.execute


#
# Custom hooks
#


class InvialidTestConfig(RuntimeError):
    pass


def pytest_sessionstart(session):
    if "tests" not in configs.ddb_table_name:
        raise InvialidTestConfig(
            "Your DynamoDB table is either not configured or not pointing to a test instance. Please check your configuration."
        )
