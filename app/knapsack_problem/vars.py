from pyomo.core import ConcreteModel
from pyomo.environ import Var, Binary

from knapsack_problem.input import ModelInput


class ModelVars:
    def __init__(
            self,
            model: ConcreteModel,
            model_input: ModelInput,
    ):
        self.model = model
        self.input = model_input
        self.make_vars()

    def make_vars(self):
        self.make_item_choose_vars()

    def make_item_choose_vars(self):
        self.model.var_z_item_choose = Var(
            self.input.items,
            domain=Binary,
            doc="Индикатор выбора предмета"
        )
