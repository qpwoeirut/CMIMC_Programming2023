"""
Edit this file! This is the file you will submit.
"""


# The function called for maze pattern 1
def carnegie_1(x, y, walls_horizontal, clock_times):
    MAZE_SIZE = 32
    VIEW_SIZE = 8

    # Greedily move up
    steps = 0
    while y + steps < MAZE_SIZE - 1 and steps < 7:
        if walls_horizontal[VIEW_SIZE][VIEW_SIZE + steps + 1] == 1:
            break
        steps = steps + 1

    return steps, 5


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
# classic wall-following strategy for mazes. maintain the direction we're going in and always turn left if possible
def carnegie_3(x: int, y: int, walls_horizontal: list[list[int]], clock_times: list[int]) -> tuple[int, int]:
    MAZE_SIZE = 32
    VIEW_SIZE = 8

    if clock_times[-1] < 5:
        current_dir = 0  # start going up
    else:
        current_dir = clock_times[-1] - 5  # 0 -> up, 1 -> down

    if current_dir == 0:  # up
        dy = 1 if y + 1 < MAZE_SIZE and walls_horizontal[VIEW_SIZE][VIEW_SIZE + 1] == 0 else 0
    elif current_dir == 1:  # down
        dy = -1 if y > 0 and walls_horizontal[VIEW_SIZE][VIEW_SIZE] == 0 else 0
    else:
        raise ValueError("this should never happen")

    next_dir = current_dir if dy == 0 else current_dir ^ 1
    return dy, next_dir + 5
