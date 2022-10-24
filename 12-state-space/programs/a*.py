# block is_valid
def is_valid(position):
    x, y = position
    return maze[y][x] != "#"
# endblock

# block next_states
def next_states(position):
    x, y = position
    states = []

    for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
        nx = x + dx
        ny = y + dy

        if is_valid((nx, ny)):
            states.append((nx, ny))

    return states
# endblock

# block bfs
def bfs(starting_state, stop_condition):
    queue = [starting_state]
    discovered = {starting_state}

    while len(queue) != 0:
        current = queue.pop(0)

        if stop_condition(current):
            print("Solution found!")
            return

        for next_state in next_states(current):
            if next_state not in discovered:
                queue.append(next_state)
                discovered.add(current)

    print("No solution!")
# endblock

# block bfs_mid
def bfs(starting_state, stop_condition):
    queue = [starting_state]
    discovered = {starting_state: None}

    while len(queue) != 0:
        current = queue.pop(0)

        if stop_condition(current):
            print("Solution found!")
            return

        for next_state in next_states(current):
            if next_state not in discovered:
                queue.append(next_state)
                discovered[next_state] = current

    print("No solution!")
# endblock

# block a_star
def a_star(starting_state, stop_condition, heuristic):
    import heapq

    heap = [(0 + heuristic(starting_state), starting_state)]
    discovered = {starting_state: None}

    i = 0
    while len(heap) != 0:
        i += 1
        distance, current = heapq.heappop(heap)

        if stop_condition(current):
            print(f"Solution found in {i} steps!")

            path = [current]
            while discovered[current] is not None:
                current = discovered[current]
                path.append(current)

            for coordinate in reversed(path):
                print(coordinate)

            return

        for next_state in next_states(current):
            if next_state not in discovered:
                next_distance = distance - heuristic(current) + 1 + heuristic(next_state)

                heapq.heappush(heap, (next_distance, next_state))
                discovered[next_state] = current

    print("No solution!")
# endblock

# block start
maze = [
    "##########",
    "#       E#",
    "#   #   ##",
    "# T #    #",
    "#   #    #",
    "#   #    #",
    "#   #    #",
    "#  #     #",
    "##########",
]

theseus = None
escape = None

for y, row in enumerate(maze):
    for x, char in enumerate(row):
        if char == "T":
            theseus = (x, y)
        elif char == "E":
            escape = (x, y)

def distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

a_star(theseus, lambda state: state == escape, lambda state: distance(state, escape))
# endblock
