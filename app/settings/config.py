from dataclasses import dataclass
from typing import Dict
import yaml


@dataclass
class SqLiteStorage:
    table_name: str
    file_path: str
    columns_typing: Dict[str, str]


@dataclass
class Config:
    storage: SqLiteStorage
    @classmethod
    def load(cls, path: str) -> "Config":
        with open(path, "r") as file:
            yaml_data = yaml.safe_load(file)

        storage = SqLiteStorage(
            table_name=yaml_data['storage']['table_name'],
            file_path=yaml_data['storage']['file_path'],
            columns_typing=yaml_data['storage']['columns_typing']
        )

        return Config(storage=storage)
