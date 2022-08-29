maze = [
    "##########",
    "#       E#",
    "#   #   ##",
    "# T #    #",
    "#   #    #",
    "#   # M  #",
    "#   #    #",
    "#  #     #",
    "##########",
]

minotaur = None
theseus = None
escape = None

for y, row in enumerate(maze):
    for x, char in enumerate(row):
        if char == "M":
            minotaur = (x, y)
        elif char == "T":
            theseus = (x, y)
        elif char == "E":
            escape = (x, y)


def is_valid(x, y):
    """Return True if the coordinates are valid."""
    return maze[y][x] != "#"


def next_theseus_moves(x, y):
    """Return next possible Theseus moves."""
    moves = []

    for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
        nx = x + dx
        ny = y + dy

        if is_valid(nx, ny):
            moves.append((nx, ny))

    return moves


def sign(value):
    return 1 if value > 0 else -1 if value < 0 else 0


def next_minotaur_position(mx, my, tx, ty):
    for _ in range(2):
        dx = sign(tx - mx)

        if is_valid(mx + dx, my):
            mx += dx
            continue

        dy = sign(ty - my)

        if is_valid(mx, my + dy):
            my += dy
            continue

    return (mx, my)


def next_states(state):
    """Generate next states from the current one."""

    (mx, my), (tx, ty) = state

    states = []

    for next_theseus in next_theseus_moves(tx, ty):
        next_minotaur = next_minotaur_position(mx, my, *next_theseus)

        if next_theseus == next_minotaur:
            continue

        states.append((next_minotaur, next_theseus))

    return states

# def search_state_space(initial_state, next_states, stop_condition):
#    discovered = dict()
#    pending = [initial_state]
#
#    while len(pending) != 0:
#        current_state = pending.pop(0)
#
#        if stop_condition(current_state):
#            path = [current_state]
#
#            while current_state in discovered:
#                path.append(current_state)
#                current_state = discovered[current_state]
#            path.append(current_state)
#
#            for state in reversed(path):
#                print(state)
#
#            quit()
#
#        for next_state in next_states(current_state):
#            if next_state not in discovered:
#                pending.append(next_state)
#                discovered[next_state] = current_state


def stop_condition(state):
    minotaur, theseus = state
    return theseus == escape


def search_state_space(initial_state, stop_condition):
    discovered = dict()
    pending = [initial_state]

    while len(pending) != 0:
        state = pending.pop(0)

        if stop_condition(state):
            path = []

            while state in discovered:
                path.append(state)
                state = discovered[state]

            path.append(initial_state)

            for state in reversed(path):
                print(state)

            quit()

        for next_state in next_states(state):
            if next_state not in discovered:
                pending.append(next_state)
                discovered[next_state] = state


search_state_space((minotaur, theseus), stop_condition)
