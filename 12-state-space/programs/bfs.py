# block is_valid
def is_position_valid(position):
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

        if is_position_valid((nx, ny)):
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

# block bfs_better
def bfs(starting_state, stop_condition):
    queue = [starting_state]
    discovered = {starting_state: None}

    while len(queue) != 0:
        current = queue.pop(0)

        if stop_condition(current):
            print("Solution found!")

            path = [current]
            while discovered[current] is not None:
                current = discovered[current]
                path.append(current)

            for coordinate in reversed(path):
                print(coordinate)

            return

        for next_state in next_states(current):
            if next_state not in discovered:
                queue.append(next_state)
                discovered[next_state] = current

    print("No solution!")
# endblock

# block bfs_deque
from collections import deque

def bfs(starting_state, stop_condition):
    queue = deque([starting_state])
    discovered = {starting_state: None}

    while len(queue) != 0:
        current = queue.popleft()

        if stop_condition(current):
            print("Solution found!")

            path = [current]
            while discovered[current] is not None:
                current = discovered[current]
                path.append(current)

            for coordinate in reversed(path):
                print(coordinate)

            return

        for next_state in next_states(current):
            if next_state not in discovered:
                queue.append(next_state)
                discovered[next_state] = current

    print("No solution!")
# endblock

# block start
maze = [
    "##########",
    "# #     E#",
    "# # # ####",
    "# T #    #",
    "### # ## #",
    "#   #    #",
    "## ## # ##",
    "#  #  #  #",
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

bfs(theseus, lambda state: state == escape)
# endblock

# block output
Solution found!
(2, 3)
(3, 3)
(3, 2)
(3, 1)
(4, 1)
(5, 1)
(6, 1)
(7, 1)
(8, 1)
# endblock
