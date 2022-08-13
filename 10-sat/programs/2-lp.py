from pulp import *


model = LpProblem(name="lp-example", sense=LpMaximize)

# variables
a, b, c, d = [LpVariable(name=n) for n in "abcd"]

# inequalities
model += 500 * a +  10 * b + 230 * c + 10 * d <= 50
model +=  10 * a +   2 * b -   7 * c +      d <= 125
model += -50 * a           -  15 * c          <= 500

# objective function
model += 18 * a + 2 * b + 10 * c + 7 * d

# solve (and ignore the debug messages)
status = model.solve(PULP_CBC_CMD(msg=False))

print(f"Objective function: {model.objective.value()}")
print("\n".join([f"{v.name} = {v.value()}" for v in [a, b, c, d]]))
