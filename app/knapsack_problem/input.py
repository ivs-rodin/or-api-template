import os
from dataclasses import dataclass
from typing import Dict, List

import pandas as pd
import json


@dataclass
class ModelConfig:
    __slots__ = (
        'max_cost',
    )

    # Максимальная стоимость рюкзака
    max_cost: float

    @classmethod
    def create_from_dict(cls, config_dict: dict):
        return cls(
            config_dict['max_cost'],
        )

    def to_json(self, output_folder: str) -> None:
        with open(os.path.join(output_folder, 'config.json'), 'w') as out_json:
            json.dump({
                attr_name: getattr(self, attr_name) for attr_name in self.__slots__
            }, out_json, indent=4)


class ModelInput:
    def __init__(self, input_folder: str):
        self.input_folder: str = input_folder
        self.config: ModelConfig = self.read_config_json()
        self.costs_dict: Dict[int, float] = self.read_costs_xlsx()
        self.items: List[int] = list(self.costs_dict.keys())

    def read_config_json(self) -> ModelConfig:
        with open(os.path.join(self.input_folder, 'config.json')) as f:
            config = ModelConfig.create_from_dict(json.load(f))
        return config

    def read_costs_xlsx(self) -> Dict[int, float]:
        costs_dict = pd.read_excel(os.path.join(self.input_folder, 'costs.xlsx'), sheet_name='Sheet1')\
            .set_index('id')['cost']\
            .to_dict()
        return costs_dict


if __name__ == '__main__':
    input_folder = os.path.join('scenarios', 'test')
    model_input = ModelInput(input_folder)

