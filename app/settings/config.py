from dataclasses import dataclass, field
from typing import cast, Dict, List
from dacite.core import from_dict
from dacite.data import Data

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
        return from_dict(Config, cast(Data, yaml_data))
