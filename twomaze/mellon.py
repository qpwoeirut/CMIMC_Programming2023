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
def mellon_3(x: int, y: int, walls_vertical: list[list[int]], clock_times: list[int]) -> tuple[int, int]:
    MAZE_SIZE = 32
    VIEW_SIZE = 8

    if clock_times[-1] < 5:
        current_dir = 0  # start going right
    else:
        current_dir = clock_times[-1] - 5  # 0 -> right, 1 -> left

    if current_dir == 0:  # right
        dx = 1 if x + 1 < MAZE_SIZE and walls_vertical[VIEW_SIZE + 1][VIEW_SIZE] == 0 else 0
    elif current_dir == 1:  # left
        dx = -1 if x > 0 and walls_vertical[VIEW_SIZE][VIEW_SIZE] == 0 else 0
    else:
        raise ValueError("this should never happen")

    next_dir = current_dir ^ 1 if dx == 0 else current_dir
    return dx, next_dir + 5