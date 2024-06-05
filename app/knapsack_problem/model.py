from pyomo.core import ConcreteModel
from pyomo.opt import SolverFactory

from knapsack_problem.constraints import ModelConstraints
from knapsack_problem.input import ModelInput
from knapsack_problem.objective import ModelObjective
from knapsack_problem.output import ModelOutput
from knapsack_problem.vars import ModelVars


class Model:
    def __init__(self, model_input: ModelInput):
        self.model = ConcreteModel()
        self.model_input = model_input
        self.vars = ModelVars(
            model=self.model,
            model_input=self.model_input,
        )
        self.constraints = ModelConstraints(
            model=self.model,
            model_input=self.model_input,
            model_vars=self.vars
        )
        self.objective = ModelObjective(
            model=self.model,
            model_input=self.model_input,
            model_vars=self.vars
        )
        self.output = ModelOutput(
            model=self.model,
            model_input=self.model_input,
            model_vars=self.vars,
            model_objective=self.objective,
        )
        self.set_parameters()

    def set_parameters(self):
        self.model.opt = SolverFactory('appsi_highs')

    def solve(self):
        self.model.opt.solve(self.model, tee=True)
        return self.output.get_solution()



