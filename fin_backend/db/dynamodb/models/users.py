from dataclasses import dataclass
from .common import BaseDDB


@dataclass
class User(BaseDDB):
    id: str
    email: str
    username: str
    name: str
