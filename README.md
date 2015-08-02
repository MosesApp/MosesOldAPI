## Moses-Webservice

## Overview
About Moses.

## API
### Description

#### User

Method |          Endpoint           | Description
-------|-----------------------------|-------------
GET    | /users                      | Returns list of users.
GET    | /users/{facebook_id}        | Gets the user with the given ID.
GET    | /users/byGroup/{group_id}   | Returns list of users from the group.
POST   | /users                      | Creates user. Returns the created user.


#### Group

Method |         Endpoint            | Description
-------|-----------------------------|-------------
GET    | /groups                     | Returns list of groups.
GET    | /groups/byUser/{user_id}    | Returns list of groups from the user.
POST   | /groups                     | Creates a group. Returns the created group.
POST   | /groups/addUser             | Adds User to group. Returns *Change?*


#### Bill

Method |         Endpoint            | Description
-------|-----------------------------|-------------
POST   | /bills                      | Creates a bill. Returns the created bill.

#### Expense

Method |         Endpoint            | Description
-------|-----------------------------|-------------
GET    | /expensesByUser/{user_id}   | Returns list of expenses from user.

#### Currency

Method |        Endpoint              | Description
-------|------------------------------|-------------
GET    | /currency                    | Returns list of currencies.
POST   | /currency                    | Creates a currency. Returns the created currency.

### Examples

#### GET /users/
```json

{
"id": 1,
"name": "Carlos Moses"
}
```

## WebService

### Class Diagram
![Moses Class Diagram](https://github.com/danielmapar/MosesWebservice/blob/master/documentation/MosesClassDiagram.png)
