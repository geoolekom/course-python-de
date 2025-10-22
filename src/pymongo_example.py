from typing import Any
from pymongo import MongoClient


MONGO_URL = "mongodb://root:secret@localhost:27017/"
client: MongoClient[dict[str, Any]] = MongoClient(MONGO_URL)

users_col = client.pythonde.users
r = users_col.find()
print("Users in MongoDB:")
for user in r:
    print(type(user), user)

new_user = {
    "username": "charlie",
    "email": "charlie@excample.com",
    "profile": {"age": 28, "interests": ["hiking", "photography"]},
    "orders": [{"order_id": 1, "product": "Camera", "amount": 1200}],
}

insert_result = users_col.insert_one(new_user)
print("Inserted user ID:", insert_result.inserted_id)
