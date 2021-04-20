from pulp import *

model = LpProblem(sense=LpMaximize)

x, y = LpVariable("x"), LpVariable("y")

model += y >= 5*x - 10
model += y <= 1/2*x + 3

model += x + 3 * y

status = model.solve(PULP_CBC_CMD(msg=False))

print("x:", x.value())
print("y:", y.value())
