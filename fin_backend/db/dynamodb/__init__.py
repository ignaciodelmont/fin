import boto3
from fin_backend import configs
from ..dynamodb.resolvers import UsersResolvers, TransactionsResolvers


class DDBClientWrapper:
    def __init__(self, client):
        self.client = client

    def put_item(self, request):
        # TODO: Put this func somewhere else
        def _convert_enums_to_strings(dictionary):
            """
            Convert any Enums in the dictionary to strings recursively
            without mutating the original dictionary.
            """
            new_dict = {}
            for key, value in dictionary.items():
                if hasattr(value, "value"):
                    new_dict[key] = value.value
                elif isinstance(value, dict):
                    new_dict[key] = _convert_enums_to_strings(value)
                else:
                    new_dict[key] = value
            return new_dict

        self.client.put_item(**_convert_enums_to_strings(request))
        return request["Item"]

    def get_item(self, request):
        response = self.client.get_item(**request)
        return response.get("Item")

    def scan(self):
        return self.client.scan()["Items"]

    def query(self, request):
        # TODO: Paginate through the results by default to overcome the 1MB limit?
        return self.client.query(**request)["Items"]

    def batch_writer(self):
        return self.client.batch_writer()

    def delete_item(self, request):
        return self.client.delete_item(**request)


class DDBFinClient:
    users: UsersResolvers = None
    client: DDBClientWrapper = None

    def __init__(self):
        self.table_name = configs.ddb_table_name
        self.client = DDBClientWrapper(
            boto3.resource("dynamodb").Table(self.table_name)
        )
        self.users = UsersResolvers(self.client)
        self.transactions = TransactionsResolvers(self.client)
