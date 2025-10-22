from mongoengine import (
    Document,
    StringField,
    IntField,
    EmbeddedDocument,
    EmbeddedDocumentField,
    DateTimeField,
    connect,
    ListField,
    EmbeddedDocumentListField,
)
from datetime import datetime

MONGO_URL = "mongodb://root:secret@localhost:27017/"
connect("pythonde", host=MONGO_URL)


class Order(EmbeddedDocument):  # type: ignore[misc]
    order_id = IntField(required=True)
    product = StringField(required=True)
    amount = IntField(min_value=0)


class Profile(EmbeddedDocument):  # type: ignore[misc]
    age = IntField(min_value=0, max_value=120)
    city = StringField(max_length=100)
    interests = ListField(StringField())


class User(Document):  # type: ignore[misc]
    meta = {"collection": "users", "indexes": ["username", "email"]}

    username = StringField(required=True, unique=True, max_length=50)
    email = StringField(required=True)
    profile = EmbeddedDocumentField(Profile)
    created_at = DateTimeField(default=datetime.utcnow)

    orders = EmbeddedDocumentListField(Order)


result = User.objects()
for engine_user in result:
    print("MongoEngine User:", engine_user.username, engine_user.profile.city)
