from pulp import *

load_capacity = 104
weights = [ 25,  35,  45,  5, 25, 3, 2, 2]
prices  = [350, 400, 450, 20, 70, 8, 5, 5]
n = len(weights)

model = LpProblem(sense=LpMaximize)

variables = [LpVariable(name=f"x{i}", cat='Binary') for i in range(n)]

model += lpSum([weights[i] * variables[i] for i in range(n)]) \
      <= load_capacity

model += lpSum([prices[i] * variables[i] for i in range(n)])

status = model.solve(PULP_CBC_CMD(msg=False))

print("optimum:", int(model.objective.value()))
print("things to take:", *[int(variables[i].value()) for i in range(n)])
