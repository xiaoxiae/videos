from pulp import *
from random import random


model = LpProblem(name="lp-sat", sense=LpMaximize)

# literal variables
variables = [LpVariable(name=c) for c in "ab"]
a, b = variables

# clause variables
x, y, z = [LpVariable(name=c) for c in "xyz"]

# inequalities
model += x <= a                  # [a]
model += y <= (1 - a) + b        # [~a, b]
model += z <= (1 - a) + (1 - b)  # [~a, ~b]

model += 0 <= a <= 1
model += 0 <= b <= 1
model += 0 <= x <= 1
model += 0 <= y <= 1
model += 0 <= z <= 1

# maximize clause variables
model += x + y + z

# solve (and ignore debug messages)
status = model.solve(PULP_CBC_CMD(msg=False))
print(f"Objective function: {model.objective.value()}")
print("Hints:", *[f"{v.name} = {v.value()}" for v in variables])
