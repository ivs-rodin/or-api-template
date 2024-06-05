from pyomo.core import ConcreteModel, Constraint, quicksum

from knapsack_problem.input import ModelInput
from knapsack_problem.vars import ModelVars
from knapsack_problem.utils import constraints_from_dict


class ModelConstraints:
    def __init__(
            self,
            model: ConcreteModel,
            model_input: ModelInput,
            model_vars: ModelVars,
    ):
        self.model = model
        self.input = model_input
        self.vars = model_vars
        self.make_constraints()

    def make_constraints(self):
        self.max_cost_constraint()

    def max_cost_constraint(self):
        max_cost_cons = {}
        max_cost_cons['max'] = (
            quicksum(
                self.model.var_z_item_choose[item_id] * self.input.costs_dict[item_id]
                for item_id in self.input.items
            )
            <=
            self.input.config.max_cost
        )
        constraints_from_dict(self.model, max_cost_cons, 'max_cost_cons')
