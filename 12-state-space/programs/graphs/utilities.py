from collections import deque

def get_tree(depth):

    def can_build_robot(ores, cost):
        for o, c in zip(ores, cost):
            if o < c:
                return False
        return True

    def next_states(remaining, ores, robots, blueprint):
        """Return the next state, given the current ores and robots."""
        states = [(list(ores), list(robots))]

        # attempt to build more robots
        # we're assuming that we can built at most one each turn
        for i, cost in enumerate(blueprint):
            if can_build_robot(ores, cost):
                states.append(
                    (
                        [o - c - (0 if i != j else 1)
                         for j, (o, c) in enumerate(zip(ores, cost))],
                        [r + (0 if i != j else 1)
                         for j, r in enumerate(robots)],
                    )
                )

        for (ores, robots) in states:
            for i in range(len(ores)):
                ores[i] += robots[i]

            yield remaining - 1, tuple(ores), tuple(robots)


    blueprint = """Blueprint 1: Each ore robot costs 4 ore.  Each clay robot costs 2 ore.  Each obsidian robot costs 3 ore and 14 clay.  Each geode robot costs 2 ore and 7 obsidian."""
    parts = blueprint.strip().split()

    # robot costs
    blueprint = (
        (
            (int(parts[6]), 0, 0, 0), # ore
            (int(parts[12]), 0, 0, 0), # clay
            (int(parts[18]), int(parts[21]), 0, 0),  # obsidian
            (int(parts[27]), 0, int(parts[30]), 0),  # geode
        )
    )

    #                   Ores        Robots
    #               Or Cl Ob Ge   Or Cl Ob Ge
    queue = deque([(depth, (0, 0, 0, 0), (1, 0, 0, 0))])
    visited = {queue[0]: None}

    while len(queue) != 0:
        current = queue.popleft()

        if current[0] == 0:
            continue

        for next_state in next_states(*current, blueprint):
            if next_state not in visited:
                queue.append(next_state)
                visited[next_state] = current
            else:
                print(visited[next_state], next_state, current)
                quit()


    for k, v in visited.items():
        if v == None:
            visited[k] = visited[k]
            break

for i in range(100):
    print(i)
    get_tree(i)
