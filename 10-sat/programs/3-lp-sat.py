from pulp import *


model = LpProblem(name="lp-sat", sense=LpMaximize)

# literal variables
a, b, c = [LpVariable(name=c, cat=LpBinary) for c in "abc"]

# clause variables
w, x, y, z = [LpVariable(name=c, cat=LpBinary) for c in "wxyz"]

# inequalities
model += w <= a           # [a]
model += x <= (1 - a)     # [~a]
model += y <= b + (1 - c) # [b, ~c]
model += z <= c           # [c]

# maximize clause variables
model += w + x + y + z

status = model.solve(PULP_CBC_CMD(msg=False))
print(f"Objective function: {model.objective.value()}")
print("\n".join([f"{v.name} = {v.value()}" for v in [a, b, c]]))
