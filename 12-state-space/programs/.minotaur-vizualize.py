maze = [
"#########################################",
"#       #   # #             # #         #",
"### # # # # # ### ### ####### # ####### #",
"#   # # # # # # # #             #     # #",
"####### # ### # ##### ####### ##### #####",
"# #       #   #   #     #   # # #       #",
"# ####### ### # ##### ### ##### # ##### #",
"#   #                 # # # # #   # #   #",
"### ##### ####### ### # # # # # ### ### #",
"#     #   #   # #   #T       M        # #",
"# ### ### # ### ##### ### # # # ### #####",
"# #       #           #   # # #   #     #",
"# ##### # # # # ### ### # # ########### #",
"#   #   # # # #   # #   # #   # # # #   #",
"####### ### ####### ### ### ### # # #####",
"#     #   #   #     #     #           # E",
"# ### # ### ### # # ### # ### ##### # # #",
"# #   # #     # # # #   # # #     # #   #",
"##### # # # ### # ### ### # # # ### # # #",
"#       # #   # # #   #     # #   # # # #",
"#########################################",
]

theseus = None
minotaur = None
escape = None

for y, row in enumerate(maze):
    for x, char in enumerate(row):
        if char == "T":
            theseus = (x, y)
        elif char == "M":
            minotaur = (x, y)
        elif char == "E":
            escape = (x, y)

def pprint(maze, t, m):
    for y, row in enumerate(maze):
        for x, column in enumerate(row):
            if (x, y) == t:
                print("T", end="")
            elif (x, y) == m:
                print("M", end="")
            else:
                print(" " if column != "#" else "#", end="")

        print()
    print()


def is_valid(position):
    x, y = position
    return maze[y][x] != "#"


def next_theseus_moves(position):
    x, y = position
    moves = []

    for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
        nx = x + dx
        ny = y + dy

        if is_valid((nx, ny)):
            moves.append((nx, ny))

    return moves


def sign(value):
    """Returns -1 if a number is negative, 1 if it's positive, else 0."""
    return -1 if value < 0 else 1 if value > 0 else 0


def next_minotaur_move(t_position, m_position):
    tx, ty = t_position
    mx, my = m_position

    for _ in range(2):
        dx = sign(tx - mx)
        if dx != 0 and is_valid((mx + dx, my)):
            mx += dx
            continue

        dy = sign(ty - my)
        if dy != 0 and is_valid((mx, my + dy)):
            my += dy
            continue

    return (mx, my)


def next_moves(state):
    (tx, ty), (mx, my) = state

    moves = []
    for new_tx in next_theseus_moves((tx, ty)):
        new_mx = next_minotaur_move(new_tx, (mx, my))

        if new_tx == new_mx:
            continue

        else:
            moves.append((new_tx, new_mx))

    return moves


def stop_condition(state):
    t_position, m_position = state
    return t_position == escape


def bfs(starting):
    queue = [starting]
    discovered = {starting: None}

    while len(queue) != 0:
        current = queue.pop(0)

        if stop_condition(current):
            path = []
            while discovered[current] is not None:
                path.append(current)
                current = discovered[current]
            path.append(current)

            for coordinate in reversed(path):
                pprint(maze, *coordinate)

            quit()

        for next_move in next_moves(current):
            if next_move not in discovered:
                discovered[next_move] = current
                queue.append(next_move)

    print("No solution!")
    quit()

bfs((theseus, minotaur))
