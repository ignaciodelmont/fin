add_user = """
mutation ($name: String!, $username: String!, $email: String!) {
  addUser(name: $name, username: $username, email: $email) {
    id
    name
    username
    email
    createdAt
    modifiedAt
}
}
"""

user = """
query ($email: String!) {
  user(email: $email) {
    id
    name
    username
    email
    createdAt
  }
}
"""


add_income = """
mutation ($amount: Decimal!, $currency: Currency!, $name: String!, $description: String) {
    addIncome(amount: $amount, currency: $currency, name: $name, description: $description) {
    id
    amount
    currency
    name
    description
}
}
"""

add_expense = """
mutation ($amount: Decimal!, $currency: Currency!, $name: String!, $description: String) {
    addExpense(amount: $amount, currency: $currency, name: $name, description: $description) {
    id
    amount
    currency
    name
    description
}
}
"""


transactions = """
query {transactions {
  id
  amount
  currency
  __typename
  createdAt
}}
"""
