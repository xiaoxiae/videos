import numpy as np
import matplotlib.pyplot as plt

with open("benchmark.txt") as f:
    lines = f.read().splitlines()

lines = lines[3:]
data = []

i = 0
while i < len(lines):
    n = int(lines[i].split()[-1][:-1])
    insert = float(lines[i + 2].split()[-1][:-3]) / 1000000 * 1e3
    search = float(lines[i + 2 + 6].split()[-1][:-3]) / 1000000 * 1e3
    delete = float(lines[i + 2 + 6 + 6].split()[-1][:-3]) / 1000000 * 1e3

    data.append((n, insert, search, delete))

    i += 19

data = np.array(data)

print(data)

fig, ax = plt.subplots()
ax.plot(data[:,0], data[:,1], label="Insert")
ax.plot(data[:,0], data[:,2], label="Search")
ax.plot(data[:,0], data[:,3], label="Delete")

ax.legend()

plt.xscale("log")

ax.set_xlabel(r'Value for $a$ ($b = 2a$)')
ax.set_xticks(data[:,0])
ax.set_xticklabels([int(d) for d in data[:,0]])
ax.set_ylabel(r'Average operation time (in $\mu s$)')

plt.gcf().set_size_inches(9, 6)
plt.show()
