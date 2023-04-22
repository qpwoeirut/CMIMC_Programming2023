"""
Edit this file! This is the file you will submit.
"""

# The function called for maze pattern 1
def mellon_1(x, y, walls_vertical, clock_times):
    MAZE_SIZE = 32
    VIEW_SIZE = 8

    # Greedily move right
    steps = 0
    while (x + steps < MAZE_SIZE - 1 and steps < 7):
        if (walls_vertical[VIEW_SIZE + steps + 1][VIEW_SIZE] == 1):
            break
        steps = steps + 1

    return (steps, 5)

# The function called for maze pattern 2
def mellon_2(x, y, walls_vertical, clock_times):
    MAZE_SIZE = 32
    VIEW_SIZE = 8

    # Greedily move right
    steps = 0
    while (x + steps < MAZE_SIZE - 1 and steps < 7):
        if (walls_vertical[VIEW_SIZE + steps + 1][VIEW_SIZE] == 1):
            break
        steps = steps + 1

    return (steps, 5)

# The function called for maze pattern 3
def mellon_3(x, y, walls_vertical, clock_times):
    MAZE_SIZE = 32
    VIEW_SIZE = 8

    # Greedily move right
    steps = 0
    while (x + steps < MAZE_SIZE - 1 and steps < 7):
        if (walls_vertical[VIEW_SIZE + steps + 1][VIEW_SIZE] == 1):
            break
        steps = steps + 1

    return (steps, 5)
