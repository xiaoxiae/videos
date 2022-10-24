# block is_valid
def is_valid(p):
    return 0 <= p <= len(bridge) - 1 and bridge[p] != " "
# endblock

# block next_states
def next_states(state):
    states = []

    for length in [2, 3, 5, 7]:
        for direction in [-1, 1]:
            new_state = state + length * direction

            if is_valid(new_state):
                states.append(new_state)

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
bridge = "# #  # #   #  #  ##"

bfs(0, lambda state: state == len(bridge) - 1)
# endblock

