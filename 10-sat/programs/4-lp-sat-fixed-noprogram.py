from pulp import *


model = LpProblem(name="lp-sat", sense=LpMaximize)

# literal variables
a, b = [LpVariable(name=c, lowBound=0, upBound=1) for c in "ab"]

# clause variables
x, y, z = [LpVariable(name=c, lowBound=0, upBound=1) for c in "xyz"]

# inequalities
model += x <= a
model += y <= (1 - a) + b
model += z <= (1 - a) + (1 - b)

# maximize clause variables
model += x + y + z

# solve (and ignore debug messages)
status = model.solve(PULP_CBC_CMD(msg=False))
print(f"Objective function: {model.objective.value()}")
print("\n".join([f"{v.name} = {v.value()}" for v in [a, b]]))
