
# Design

## Transactions

| Type    | pk                     | sk                  | created_at  | modified_at | amount | description |
| --- | --- | --- | --- | --- | --- | --- | 
| Income  | TRANSACTION#<user_id> | <timestamp>#INCOME  | <timestamp> | <timestamp> |        |             |
| Expense | TRANSACTION#<user_id> | <timestamp>#EXPENSE | <timestamp> | <timestamp> |        |             |


## User

- User `id` is unique and `email` is unique too. We index by `email` to avoid collisions but if user wants to update it's email we `REMOVE` the obj and insert a new one with a different `sk`, and same `id`. All references to the user are by `id`


| Type | pk   | sk        | id     | created_at  | modified_at | username | email | first_name | last_name | gsi1pk     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| User | USER | <username> | <uuid> | <timestamp> | <timestamp> |          |       |            |           | <username> |
|      |      |           |        |             |             |          |       |            |           |            |


