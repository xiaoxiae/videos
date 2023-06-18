from pulp import *


# problem formulation
model = LpProblem(sense=LpMaximize)

x_p = LpVariable(name="potatoes", lowBound=0)
x_c = LpVariable(name="carrots", lowBound=0)

model += x_p       <= 3000  # potatoes
model +=       x_c <= 4000  # carrots
model += x_p + x_c <= 5000  # fertilizer

model += x_p * 1.2 + x_c * 1.7

# solve (without being verbose)
status = model.solve(PULP_CBC_CMD(msg=False))
print("potatoes:", x_p.value())
print("carrots:", x_c.value())
print("profit:", model.objective.value())
