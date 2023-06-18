from pulp import *


# data
n = 8
weights = [4, 2, 8, 3, 7, 5, 9, 6]
prices = [19, 17, 30, 13, 25, 29, 23, 10]
carry_weight = 17

# problem formulation
model = LpProblem(sense=LpMaximize)

variables = [LpVariable(name=f"x_{i}", cat=LpBinary) for i in range(n)]

model += lpDot(weights, variables) <= carry_weight

model += lpDot(prices, variables)

# solve (without being verbose)
status = model.solve(PULP_CBC_CMD(msg=False))
print("price:", model.objective.value())
print("take:", *[variables[i].value() for i in range(n)])
