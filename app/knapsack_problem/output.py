from pyomo.core import ConcreteModel, value

from knapsack_problem.input import ModelInput
from knapsack_problem.objective import ModelObjective
from knapsack_problem.vars import ModelVars


class ModelOutput:
    def __init__(
            self,
            model: ConcreteModel,
            model_input: ModelInput,
            model_vars: ModelVars,
            model_objective: ModelObjective,
    ):
        self.model = model
        self.input = model_input
        self.vars = model_vars
        self.objective = model_objective

    def get_solution(self):
        return {
            'chosen_items:': [item_id for item_id, var in self.model.var_z_item_choose.items() if var.value > 0.5],
            'objective_components:': {
                obj_component: value(obj_expr) for obj_component, obj_expr in self.objective.objective_components.items()
            }
        }
