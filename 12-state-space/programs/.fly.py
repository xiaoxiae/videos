maze = [
    "#######",
    "# E   #",
    "#S    #",
    "#     #",
    "#   # #",
    "##    #",
    "#    ##",
    "#######",
]

start = None
end = None

for y, row in enumerate(maze):
    for x, char in enumerate(row):
        if char == "S":
            start = (x, y)
        elif char == "E":
            end = (x, y)


def is_valid(x, y):
    """Return True if the coordinates are valid."""
    return maze[y][x] != "#"


def next_states(state):
    x, y = state
    moves = []

    for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
        nx = x + dx
        ny = y + dy

        while is_valid(nx, ny):
            nx += dx
            ny += dy

        nx -= dx
        ny -= dy

        moves.append((nx, ny))

    return moves


def stop_condition(state):
    return state == end


def search_state_space(initial_state, stop_condition, next_states):
    discovered = {initial_state: initial_state}
    pending = [initial_state]

    while len(pending) != 0:
        state = pending.pop(0)

        if stop_condition(state):
            path = []

            while discovered[state] != state:
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


search_state_space(start, stop_condition, next_states)
