from pulp import *

edges = [(1,2), (3,2), (2,4), (1,4), (2,5), (6,5), (3,6), (1,5)]
n = len(set([u for u, v in edges] + [v for u, v in edges]))

model = LpProblem(sense=LpMinimize)

chromatic_number = LpVariable(name="chromatic number", cat='Integer')
variables = [[LpVariable(name=f"x_{i}_{j}", cat='Binary') \
              for i in range(n)] for j in range(n)]

for i in range(n):
    model += lpSum(variables[i]) == 1
for u, v in edges:
    for color in range(n):
        model += variables[u - 1][color] + variables[v - 1][color] <= 1
for i in range(n):
    for j in range(n):
        model += chromatic_number >= (j + 1) * variables[i][j]

model += chromatic_number

status = model.solve(PULP_CBC_CMD(msg=False))

print("chromatic number:", int(chromatic_number.value()))
print("\n".join([f"vertex {i} has color {j}" \
      for i in range(n) for j in range(n) if variables[i][j].value()]))
