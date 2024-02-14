from .common import BaseDDB
from typing import Optional
from dataclasses import dataclass


@dataclass
class Label(BaseDDB):
    name: str
    description: Optional[str] = None
