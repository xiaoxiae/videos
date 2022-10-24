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


# block next_theseus_positions
def move_towards(start, end):
    return +1 if start < end else 0 if start == end else -1

def next_minotaur_position(t_pos, m_pos):
    tx, ty = t_pos
    mx, my = m_pos

    for _ in range(2):
        dx = move_towards(mx, tx)  # horizontal movement
        if dx != 0 and is_valid((mx + dx, my)):
            mx += dx
            continue

        dy = move_towards(my, ty)  # vertical movement
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

def distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

a_star((theseus, minotaur), lambda state: state[0] == escape, lambda state: distance(state[0], escape))
# endblock
