# block is_valid
def is_valid(position):
    x, y = position
    return maze[y][x] != "#"
# endblock

# block next_theseus_positions
def next_theseus_positions(position):
    x, y = position
    states = []

    for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
        nx = x + dx
        ny = y + dy

        if is_valid((nx, ny)):
            states.append((nx, ny))

    return states
# endblock


# block next_minotaur_position
def move_towards(m, t):
    return +1 if m < t else 0 if m == t else -1

def next_minotaur_position(t_pos, m_pos):
    tx, ty = t_pos
    mx, my = m_pos

    for _ in range(2):
        # horizontal movement
        dx = move_towards(mx, tx)
        if dx != 0 and is_valid((mx + dx, my)):
            mx += dx
            continue

        # vertical movement
        dy = move_towards(my, ty)
        if dy != 0 and is_valid((mx, my + dy)):
            my += dy
            continue

    return (mx, my)
# endblock

# block next_states
def next_states(state):
    t_pos, m_pos = state
    states = []

    for new_t_pos in next_theseus_positions(t_pos):
        new_m_pos = next_minotaur_position(new_t_pos, m_pos)

        if new_t_pos == new_m_pos:
            continue

        states.append((new_t_pos, new_m_pos))

    return states
# endblock


# block bfs
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

# block start
maze = [
    "##########",
    "#       E#",
    "#   #   ##",
    "# T # M  #",
    "#   #    #",
    "#   #    #",
    "#   #    #",
    "#  #     #",
    "##########",
]

theseus = None
escape = None
minotaur = None

for y, row in enumerate(maze):
    for x, char in enumerate(row):
        if char == "T":
            theseus = (x, y)
        elif char == "E":
            escape = (x, y)
        elif char == "M":
            minotaur = (x, y)

bfs((theseus, minotaur), lambda state: state[0] == escape)
# endblock

# block start_partial
maze = [
    "##########",
    "#       E#",
    "#   #   ##",
    "# T # M  #",
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

bfs(theseus, lambda state: state == escape)
# endblock

# block start_partial_2
maze = [
    "##########",
    "#       E#",
    "#   #   ##",
    "# T # M  #",
    "#   #    #",
    "#   #    #",
    "#   #    #",
    "#  #     #",
    "##########",
]

theseus = None
escape = None
minotaur = None

for y, row in enumerate(maze):
    for x, char in enumerate(row):
        if char == "T":
            theseus = (x, y)
        elif char == "E":
            escape = (x, y)
        elif char == "M":
            minotaur = (x, y)

bfs(theseus, lambda state: state == escape)
# endblock

# block output
Solution found!
((2, 3), (6, 3))
((2, 4), (5, 4))
((2, 5), (5, 5))
((2, 6), (5, 6))
((2, 7), (4, 7))
((2, 6), (4, 7))
((3, 6), (4, 7))
((3, 5), (4, 7))
((3, 4), (4, 7))
((3, 3), (4, 7))
((3, 2), (4, 7))
((3, 1), (4, 7))
((4, 1), (4, 7))
((5, 1), (5, 6))
((6, 1), (6, 5))
((7, 1), (7, 4))
((8, 1), (8, 3))
# endblock
