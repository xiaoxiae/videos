import sys

sys.path.insert(0, "../")
from utilities import success, get_input

import heapq


def can_build_robot(ores, cost):
    for o, c in zip(ores, cost):
        if o < c:
            return False
    return True

def next_states(ores, robots, blueprint):
    """Return the next state, given the current ores and robots."""
    states = [(list(ores), list(robots))]

    # attempt to build more robots
    # we're assuming that we can built at most one each turn
    can_build = 0
    for i, cost in enumerate(blueprint):
        if can_build_robot(ores, cost):
            can_build += 1
            states.append(
                (
                    [o - c - (0 if i != j else 1)
                     for j, (o, c) in enumerate(zip(ores, cost))],
                    [r + (0 if i != j else 1)
                     for j, r in enumerate(robots)],
                )
            )

    # if we can build any robot, don't store resources
    if can_build == len(blueprint):
        states.pop(0)

    for (ores, robots) in states:
        for i in range(len(ores)):
            ores[i] += robots[i]

        yield tuple(ores), tuple(robots)

def can_be_best(remaining, ores, robots, max_geodes):
    """Return True if the state can beat max_geodes score."""
    # shit estimation: assume we can build a geode robot every turn
    return ((remaining * (remaining - 1)) // 2 + robots[-1] * remaining + ores[-1]) > max_geodes


total = 0
for bpid, line in enumerate(get_input()):
    parts = line.split()

    # robot costs
    blueprint = (
        (
            (int(parts[6]), 0, 0, 0), # ore
            (int(parts[12]), 0, 0, 0), # clay
            (int(parts[18]), int(parts[21]), 0, 0),  # obsidian
            (int(parts[27]), 0, int(parts[30]), 0),  # geode
        )
    )

    #                      Ores        Robots
    #                  Or Cl Ob Ge   Or Cl Ob Ge
    queue = [(0, 24, ((0, 0, 0, 0), (1, 0, 0, 0)))]
    visited = {queue[0][-1]: 24}
    max_geodes = 0

    while len(queue) != 0:
        s, remaining, (ores, robots) = heapq.heappop(queue)

        max_geodes = max(max_geodes, ores[-1])

        if remaining == 0:
            continue

        if visited[(ores, robots)] != remaining:
            continue

        if not can_be_best(remaining, ores, robots, max_geodes):
            continue

        for next_state in next_states(ores, robots, blueprint):
            if next_state not in visited or visited[next_state] < remaining - 1:
                heapq.heappush(queue, (ores[0] * 1000 + ores[1] * 100 + ores[2] * 10 + ores[3], remaining - 1, next_state))
                visited[next_state] = remaining - 1

    total += max_geodes * (bpid + 1)

success(total)
