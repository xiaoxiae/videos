from pulp import *
from utilities import *

def get_coloring(edges, one_indexing=False):
    n = len(set([u for u, v in edges] + [v for u, v in edges]))
    colors = [RED, GREEN, BLUE, PINK, ORANGE, LIGHT_BROWN]

    model = LpProblem(sense=LpMinimize)

    chromatic_number = LpVariable(name="chromatic number", cat='Integer')
    variables = [[LpVariable(name=f"x_{i}_{j}", cat='Binary') \
                  for i in range(n)] for j in range(n)]

    for i in range(n):
        model += lpSum(variables[i]) == 1
    for u, v in edges:
        for color in range(n):
            model += variables[u - (1 if one_indexing else 0)][color] + variables[v - (1 if one_indexing else 0)][color] <= 1
    for i in range(n):
        for j in range(n):
            model += chromatic_number >= (j + 1) * variables[i][j]

    model += chromatic_number

    status = model.solve(PULP_CBC_CMD(msg=False))

    return {i: colors[j]
          for i in range(n) for j in range(n) if variables[i][j].value()}
