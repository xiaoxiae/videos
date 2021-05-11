from pulp import *
from utilities import *

def get_independent_set(edges, one_indexing=False):
    n = len(set([u for u, v in edges] + [v for u, v in edges]))

    model = LpProblem(sense=LpMaximize)

    variables = [LpVariable(name=f"x_{i}", cat='Binary') for i in range(n)]

    for u, v in edges:
        model += variables[u - 1] + variables[v - 1] <= 1

    model += lpSum(variables)

    status = model.solve(PULP_CBC_CMD(msg=False))
    return [i + 1 for i in range(n) if int(variables[i].value()) == 1]
