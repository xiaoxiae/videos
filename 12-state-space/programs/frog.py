#bridge = "#### ## # ### # #  #   # #  #  ####"
bridge = "#   #  #   #"


def is_valid(p):
    return 0 <= p <= len(bridge) - 1 and bridge[p] != " "


def next_moves(p):
    moves = []

    for jump_length in [2, 3, 5, 7]:
        for direction in [-1, 1]:
            new_p = p + jump_length * direction

            if is_valid(new_p):
                moves.append(new_p)

    return moves


def stop_condition(p):
    return p == len(bridge) - 1


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

bfs(0)
