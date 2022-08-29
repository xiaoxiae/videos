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


def is_valid(position):
    x, y = position
    return maze[y][x] != "#"


def next_moves(position):
    x, y = position
    moves = []

    for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
        nx = x + dx
        ny = y + dy

        if is_valid((nx, ny)):
            moves.append((nx, ny))

    return moves


def stop_condition(position):
    return position == escape


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
                print(coordinate)

            quit()

        for next_move in next_moves(current):
            if next_move not in discovered:
                discovered[next_move] = current
                queue.append(next_move)

    print("No solution!")
    quit()

bfs(theseus)
