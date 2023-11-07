from dataclasses import dataclass
from typing import Dict
import yaml
import os


@dataclass
class SqLiteStorage:
    table_name: str
    file_path: str
    columns_typing: Dict[str, str]

@dataclass
class NLPModule:
    plug: bool
    device: str


@dataclass
class Config:
    storage: SqLiteStorage
    nlp_module: NLPModule

    @classmethod
    def load(cls) -> "Config":
        script_dir = os.path.dirname(os.path.dirname(__file__))
        config_file_path = os.path.join(script_dir, "config.yaml")
        with open(config_file_path, "r") as file:
            yaml_data = yaml.safe_load(file)

        storage = SqLiteStorage(
            table_name=yaml_data['storage']['table_name'],
            file_path=yaml_data['storage']['file_path'],
            columns_typing=yaml_data['storage']['columns_typing']
        )

        nlp_module = NLPModule(plug=yaml_data["nlp_module"]["plug"],
                               device=yaml_data['nlp_module']['device'])

        return Config(storage=storage, nlp_module=nlp_module)
