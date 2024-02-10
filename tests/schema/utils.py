from fin.schema import schema


class TestContext(dict):
    pass


def execute(query, variable_values=None, context_value=None):
    context = context_value or TestContext()
    return schema.execute_sync(query, variable_values, context_value=context).__dict__
