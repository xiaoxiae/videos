from pulp import *

import networkx as nx
edges = nx.petersen_graph().edges

# number of vertices
n = len(set([u for u, v in edges] + [v for u, v in edges]))

model = LpProblem(sense=LpMinimize)

# variables -- x_{u, v, k} depending on whether {u, v} is colored using color k
variables = {}
for i, j in edges:
    variables[(i, j)] = []

    for k in range(n):
        variables[(i, j)].append(LpVariable(name=f"x_{i}_{j}_{k}", cat='Binary'))

    variables[(j, i)] = variables[(i, j)]

# the edge chromatic number is also a variable
edge_chromatic_number = LpVariable(name="edge_edge_chromatic_number", lowBound=0, cat='Integer')

# each edge has exactly one color
for i, j in edges:
    model += lpSum(variables[(i, j)]) == 1

# each vertex' adjacent colors are different
for color in range(n):
    for u in range(n):
        model += lpSum([variables[(u, v)][color] for v in range(n) if (u, v) in variables]) <= 1

# edge chromatic number is also the number of the highest color
for i, j in edges:
    for color in range(n):
        model += edge_chromatic_number >= (color + 1) * variables[(i, j)][color]

# we're minimizing the edge chromatic number
model += edge_chromatic_number

status = model.solve(PULP_CBC_CMD(msg=False))

print(f"edge chromatic number: {int(edge_chromatic_number.value())}")
for i, j in edges:
    for color in range(n):
        if variables[(i, j)][color].value() != 0:
            print(f"{(i, j)}: {color}")
