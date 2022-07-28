from pulp import *
from random import random


model = LpProblem(name="lp-sat", sense=LpMaximize)

# literal variables
a, b, c, d, e, f = [LpVariable(name=c, cat=LpBinary) for c in "abcdef"]

# clause variables
x, y, z = [LpVariable(name=c, cat=LpBinary) for c in "xyz"]

# inequalities
model += x <= a + (1 - b) + (1 - c)  # [a, ~b, ~c]
model += y <= (1 - a) + d + e        # [~a, d, e]
model += z <= e + f                  # [e, f]

# maximize clause variables
model += x + y + z

# solve (and ignore debug messages)
status = model.solve(PULP_CBC_CMD(msg=False))
print(f"Objective function: {model.objective.value()}")
print("\n".join([f"{v.name} = {v.value()}" for v in [a, b, c, d, e, f]]))
