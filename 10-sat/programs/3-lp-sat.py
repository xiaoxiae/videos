from pulp import *
from random import random


model = LpProblem(name="lp-sat", sense=LpMaximize)

# literal variables
a, b, c, d, e, f = [LpVariable(name=c, lowBound=0, upBound=1) for c in "abcdef"]

# clause variables
x, y, z = [LpVariable(name=c, lowBound=0, upBound=1) for c in "xyz"]

# inequalities
model += x <= a + (1 - b) + (1 - c)  # [a, ~b, ~c]
model += y <= (1 - a) + d + e        # [~a, d, e]
model += z <= e + f                  # [e, f]

# maximize clause variables
model += x + y + z

# solve (and ignore debug messages)
status = model.solve(PULP_CBC_CMD(msg=False))
print(f"Objective function: {model.objective.value()}")
print("Hints:", *[f"{v.name} = {v.value()}" for v in [a, b, c, d, e, f]])


def count_satisfied_clauses(*clauses):
    """Count the number of satisfied clauses."""
    total = 0
    for clause in clauses:
        if any(clause):
            total += 1
    return total


def assign_variables_based_on_lp():
    """Return an assignment of n variables based on """
    return [False if l.value() <= random() else True for l in [a, b, c, d, e, f]]


experiments = 10000
satisfied = 0

for i in range(experiments):
    a, b, c, d, e, f = assign_variables_based_on_lp()

    satisfied += count_satisfied_clauses([a, not b, not c], [not a, d, e], [e, f])

average = satisfied / experiments

print(f"{average:.2f}/3 ~= {average/3 * 100:.2f}%")

