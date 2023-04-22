import random

def solvable(walls_horizontal, walls_vertical, size):
    """
    Check if a maze is solvable.
    """
    walls_horizontal = walls_horizontal
    walls_vertical = walls_vertical

    visited = []
    for i in range(0, size):
        visited.append([])
        for _ in range(0, size):
            visited[i].append(0)

    work = [(0, 0)]
    visited[0][0] = 1

    while (len(work) > 0):
        curr = work.pop()
        visited[curr[0]][curr[1]] = 1
        if (curr[0] == size - 1 and curr[1] == size - 1):
            return True
        if (curr[0] > 0 and (visited[curr[0]-1][curr[1]] == 0)):
            if (walls_vertical[curr[0]][curr[1]] == 0):
                work.append((curr[0]-1, curr[1]))
        if (curr[0] < size - 1 and (visited[curr[0]+1][curr[1]] == 0)):
            if (walls_vertical[curr[0]+1][curr[1]] == 0):
                work.append((curr[0]+1, curr[1]))
        if (curr[1] > 0 and (visited[curr[0]][curr[1]-1] == 0)):
            if (walls_horizontal[curr[0]][curr[1]] == 0):
                work.append((curr[0], curr[1]-1))
        if (curr[1] < size - 1 and (visited[curr[0]][curr[1]+1] == 0)):
            if (walls_horizontal[curr[0]][curr[1]+1] == 0):
                work.append((curr[0], curr[1]+1))

    return False


def generate_random(probability, size):
    """
    Randomly generate maze walls, and retry until solvable.
    """
    walls_horizontal = []
    walls_vertical = []
    for i in range(0, size):
        walls_horizontal.append([])
        walls_vertical.append([])
        for j in range(0, size):
            if (j == 0) or (random.random() < probability):  # TODO: use better rng
                walls_horizontal[i].append(1)
            else:
                walls_horizontal[i].append(0)
            if (i == 0) or (random.random() < probability):
                walls_vertical[i].append(1)
            else:
                walls_vertical[i].append(0)
    
    if not solvable(walls_horizontal, walls_vertical, size):
        return generate_random(probability, size)

    return (walls_horizontal, walls_vertical)


def generate_cycleless(size):
    """
    Generate a maze via dfs, and just in case, retry until solvable.
    """
    walls_horizontal = []
    walls_vertical = []
    visited = []
    for i in range(0, size):
        walls_horizontal.append([])
        walls_vertical.append([])
        visited.append([])
        for j in range(0, size):
            walls_horizontal[i].append(1)
            walls_vertical[i].append(1)
            visited[i].append(0)

    work = [(0, 0)]
    visited[0][0] = 1
    while (len(work) > 0):
        curr = work.pop()
        neighbor = []
        if (curr[0] > 0 and (visited[curr[0]-1][curr[1]] == 0)):
            neighbor.append(((curr[0]-1, curr[1]), 'v', 0))
        if (curr[0] < size - 1 and (visited[curr[0]+1][curr[1]] == 0)):
            neighbor.append(((curr[0]+1, curr[1]), 'v', 1))
        if (curr[1] > 0 and (visited[curr[0]][curr[1]-1] == 0)):
            neighbor.append(((curr[0], curr[1]-1), 'h', 0))
        if (curr[1] < size - 1 and (visited[curr[0]][curr[1]+1] == 0)):
            neighbor.append(((curr[0], curr[1]+1), 'h', 1))
        if (len(neighbor) == 0):
            continue
        elif (len(neighbor) > 1):
            work.append(curr)
        random.shuffle(neighbor)
        new = neighbor[0]
        if (new[1] == 'v'):
            walls_vertical[curr[0]+new[2]][curr[1]] = 0
        if (new[1] == 'h'):
            walls_horizontal[curr[0]][curr[1]+new[2]] = 0
        visited[new[0][0]][new[0][1]] = 1
        work.append(new[0])
    
    if not solvable(walls_horizontal, walls_vertical, size):
        return generate_cycleless(size)

    return (walls_horizontal, walls_vertical)
