from . import gql_queries as q


def test_add_user(execute, snapshot):
    res = execute(
        q.add_user,
        {"name": "Tester User", "email": "tester@email.com", "username": "tester"},
    )
    snapshot.assert_match(res, "Test addUser")

    res = execute(
        q.add_user,
        {
            "name": "Tester Userr",
            "email": "tester_another@email.com",
            "username": "testerr",
        },
    )
    snapshot.assert_match(res, "Test another addUser")

    res = execute(q.user, {"email": "tester@email.com"})

    snapshot.assert_match(res, "Test user query")
