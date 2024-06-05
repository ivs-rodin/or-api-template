import os

from knapsack_problem.input import ModelInput
from knapsack_problem.model import Model


def run_model(input_folder: str):
    model_input = ModelInput(input_folder)
    knapsack_problem = Model(model_input)
    result = knapsack_problem.solve()
    return result


if __name__ == '__main__':
    input_folder = os.path.join('scenarios', 'test')
    result = run_model(input_folder)
