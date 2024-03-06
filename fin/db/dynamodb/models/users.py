from dataclasses import dataclass
from .common import BaseDDB


@dataclass
class User(BaseDDB):
    email: str
    username: str
    name: str
