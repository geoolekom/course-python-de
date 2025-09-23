from typing import NamedTuple
from dataclasses import dataclass, field

# Named tuple


class User(NamedTuple):
    user_id: int
    username: str
    email: str


user = User(user_id=1, username="john doe", email="email@site.com")


# Dataclass
@dataclass
class DataClassUser:
    user_id: int
    username: str
    email: str
    is_active: bool = False
    tags: list[str] = field(default_factory=list)


data_user = DataClassUser(user_id=1, username="", email="")
print(data_user)
