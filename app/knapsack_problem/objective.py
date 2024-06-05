from pyomo.core import ConcreteModel, quicksum, maximize, Objective

from knapsack_problem.input import ModelInput
from knapsack_problem.vars import ModelVars


class ModelObjective:
    def __init__(
            self,
            model: ConcreteModel,
            model_input: ModelInput,
            model_vars: ModelVars,
    ):
        self.model = model
        self.input = model_input
        self.vars = model_vars
        self.objective_components = {}
        self.make_objective()

    def make_objective(self):
        self.objective_components['total_cost'] = self.total_cost_objective()
        self.model.objective = Objective(expr=quicksum(self.objective_components.values()), sense=maximize)

    def total_cost_objective(self):
        return quicksum(
            self.model.var_z_item_choose[item_id] * self.input.costs_dict[item_id]
            for item_id in self.input.items
        )
