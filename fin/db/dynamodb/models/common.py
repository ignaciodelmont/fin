from dataclasses import dataclass


@dataclass
class BaseDDB:
    pk: str
    sk: str
    created_at: str
    modified_at: str
    id: str

    def __getitem__(self, item):
        return getattr(self, item)

    def get(self, key):
        return self.__getitem__(key)
