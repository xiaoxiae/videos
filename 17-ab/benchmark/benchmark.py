import numpy as np
import matplotlib.pyplot as plt

with open("benchmark.txt") as f:
    lines = f.read().splitlines()

lines = lines[2:]
data = []

i = 0
N = 1_000_000
while i < len(lines):
    n = int(lines[i].split()[-1][:-1])
    insert = float(lines[i + 2].split()[-1][:-3]) / N * 1e3
    search = float(lines[i + 2 + 6].split()[-1][:-3]) / N * 1e3
    delete = float(lines[i + 2 + 6 + 6].split()[-1][:-3]) / N * 1e3

    data.append((n, insert, search, delete))

    i += 19

data = np.array(data)

n = 64

fig, ax = plt.subplots()
ax.plot(data[:,0][:n], data[:,1][:n], label="Insert")
ax.plot(data[:,0][:n], data[:,2][:n], label="Search")
ax.plot(data[:,0][:n], data[:,3][:n], label="Delete")

ax.legend()

ax.set_xlabel(r'Value for $a$ (and $b = 2a$)')
ax.set_xticks(data[:,0][:n])
ax.set_xticklabels([int(d) for d in data[:,0][:n]])
ax.set_ylabel(r'Average operation time (in $\mu s$)')

plt.gcf().set_size_inches(9, 6)
plt.show()
