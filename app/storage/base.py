from typing import Generic, TypeVar


StorageType = TypeVar("StorageType")


class StorageConnector(Generic[StorageType]):
    def __init__(self, storage_: StorageType) -> None:
        self._storage = storage_

    def get(self):
        pass

    def insert(self, data) -> None:
        pass

    def delete(self, data) -> None:
        pass
