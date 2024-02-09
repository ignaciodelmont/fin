from . import gql_queries


def test_add_transactions(execute, snapshot):
    res = execute(
        gql_queries.add_income,
        {"amount": 4000, "currency": "USD", "name": "Salary", "description": "Monthly Salary"}
    )

    snapshot.assert_match(res, "Test add Income")

    res = execute(
        gql_queries.add_expense,
        {"amount": 2000, "currency": "ARS", "name": "Pringles"}
    )

    snapshot.assert_match(res, "Test add Expense")

    res = execute(
        gql_queries.transactions, {})

    snapshot.assert_match(res, "Test transactions")
