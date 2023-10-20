from typing import Generic, TypeVar, List


StorageType = TypeVar("StorageType")


class StorageConnector(Generic[StorageType]):
    def __init__(self, storage_: StorageType) -> None:
        self._storage = storage_

    def init_client(self) -> None:
        pass

    def get(self):
        pass

    def insert(self, data) -> None:
        pass

    def post(self, data, allow_update: bool = False) -> None:
        pass

    def delete(self, data) -> None:
        pass
