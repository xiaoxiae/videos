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


def count_satisfied_clauses(*clauses):
    """Count the number of satisfied clauses."""
    total = 0
    for clause in clauses:
        if any(clause):
            total += 1
    return total


def assign_variables_based_on_lp():
    """Return an assignment of n variables based on """
    return [True if l.value() <= random() else False for l in variables]


experiments = 10000
satisfied = 0

for i in range(experiments):
    a, b = assign_variables_based_on_lp()

    satisfied += count_satisfied_clauses([a], [not a, b], [not a, not b])

average = satisfied / experiments

print(f"{average:.2f}/3 ~= {average/3 * 100:.2f}%")
