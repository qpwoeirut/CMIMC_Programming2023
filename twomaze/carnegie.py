"""
Edit this file! This is the file you will submit.
"""

# The function called for maze pattern 1
def carnegie_1(x, y, walls_horizontal, clock_times):
    MAZE_SIZE = 32
    VIEW_SIZE = 8

    # Greedily move up
    steps = 0
    while (y + steps < MAZE_SIZE - 1 and steps < 7):
        if (walls_horizontal[VIEW_SIZE][VIEW_SIZE + steps + 1] == 1):
            break
        steps = steps + 1

    return (steps, 5)

# The function called for maze pattern 2
def carnegie_2(x, y, walls_horizontal, clock_times):
    MAZE_SIZE = 32
    VIEW_SIZE = 8

    # Greedily move up
    steps = 0
    while (y + steps < MAZE_SIZE - 1 and steps < 7):
        if (walls_horizontal[VIEW_SIZE][VIEW_SIZE + steps + 1] == 1):
            break
        steps = steps + 1

    return (steps, 5)

# The function called for maze pattern 3
def carnegie_3(x, y, walls_horizontal, clock_times):
    MAZE_SIZE = 32
    VIEW_SIZE = 8

    # Greedily move up
    steps = 0
    while (y + steps < MAZE_SIZE - 1 and steps < 7):
        if (walls_horizontal[VIEW_SIZE][VIEW_SIZE + steps + 1] == 1):
            break
        steps = steps + 1

    return (steps, 5)
