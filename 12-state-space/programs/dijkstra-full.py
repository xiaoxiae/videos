from random import seed, randint

with open("../maze/mask2.txt") as f:
    maze = f.read().splitlines()


def is_valid(position):
    x, y = position
    return 0 <= x < len(maze[0]) and 0 <= y < len(maze) and maze[y][x] != "."

def next_states(position):
    x, y = position
    states = []

    for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
        nx = x + dx
        ny = y + dy

        if not is_valid((nx, ny)):
            continue

        if maze[ny][nx] == " ":
            states.append((1, (nx, ny)))
        else:
            states.append((10, (nx, ny)))

    return states


from heapq import heappush, heappop

def dijkstra(starting_state, stop_condition):
    queue = [(0, starting_state)]
    discovered = {starting_state: None}
    distance = {starting_state: 0}

    while len(queue) != 0:
        d_s2c, current = heappop(queue)

        if stop_condition(current):
            print("Solution found!")

            path = [current]
            while discovered[current] is not None:
                current = discovered[current]
                path.append(current)

            for coordinate in reversed(path):
                print(coordinate)

            return

        for d_c2n, next_state in next_states(current):
            d_s2n = d_s2c + d_c2n

            if next_state not in discovered \
            or distance[next_state] > d_s2n:
                heappush(queue, (d_s2n, next_state))

                discovered[next_state] = current
                distance[next_state] = d_s2n

    print("No solution!")

theseus = None
escape = None

for y, row in enumerate(maze):
    for x, char in enumerate(row):
        if char == "T":
            theseus = (x, y)
        elif char == "E":
            escape = (x, y)

seed(0xBADBEED3)

for i in range(len(maze)):
    maze[i] = list(maze[i])

blocks = []
for _ in range(40):
    x, y = 0, 0

    while maze[y][x] != " " or (x, y) == theseus or (x, y) == escape:
        x, y = (randint(0, len(maze[0]) - 1), randint(0, len(maze) - 1))

    maze[y][x] = "#"

dijkstra(theseus, lambda x: x == escape)
