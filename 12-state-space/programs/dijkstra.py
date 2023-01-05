# block bfs
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

# block dijkstra
from heapq import heappush, heappop

def bfs(starting_state, stop_condition):
    queue = [(0, starting_state)]
    discovered = {starting_state: None}

    while len(queue) != 0:
        d, current = heappop(queue)

        if stop_condition(current):
            print("Solution found!")

            path = [current]
            while discovered[current] is not None:
                current = discovered[current]
                path.append(current)

            for coordinate in reversed(path):
                print(coordinate)

            return

        for d_to_next, next_state in next_states(current):
            if next_state not in discovered:
                heappush(queue, (d + d_to_next, next_state))
                discovered[next_state] = current

    print("No solution!")
# endblock
