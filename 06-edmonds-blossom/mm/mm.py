from pulp import *


def get_maximum_matching(edges):
    vertices = set([u for u, v in edges] + [v for u, v in edges])

    n = len(vertices)
    m = len(edges)

    model = LpProblem(sense=LpMaximize)

    variables = {e: LpVariable(name=f"x_{e}", cat="Binary") for e in edges}

    for v in vertices:
        for a in edges:
            for b in edges:
                if v in a and v in b and a != b:
                    model += variables[a] + variables[b] <= 1

    model += lpSum([variables[e] for e in variables])

    status = model.solve(PULP_CBC_CMD(msg=False))

    return [e for e in edges if variables[e].value()]
