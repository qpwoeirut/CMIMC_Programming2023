def carnegie_1(x: int, y: int, walls_horizontal: list[list[int]], clock_times: list[int]) -> tuple[int, int]:
    return carnegie_wall_following(x, y, walls_horizontal, clock_times)


def carnegie_2(x: int, y: int, walls_horizontal: list[list[int]], clock_times: list[int]) -> tuple[int, int]:
    return carnegie_wall_following(x, y, walls_horizontal, clock_times)


# classic wall-following strategy for mazes. maintain the direction we're going in and always turn left if possible
def carnegie_3(x: int, y: int, walls_horizontal: list[list[int]], clock_times: list[int]) -> tuple[int, int]:
    return carnegie_wall_following(x, y, walls_horizontal, clock_times)


def carnegie_greedy(y: int, walls_horizontal: list[list[int]], current_dir: int) -> int:
    VIEW_SIZE = 8

    dy = 0
    if current_dir == 0:  # up
        while dy < 7:
            if walls_horizontal[VIEW_SIZE][VIEW_SIZE + dy + 1] == 1:
                break
            dy += 1
    else:  # down
        while dy > -7:
            if walls_horizontal[VIEW_SIZE][VIEW_SIZE + dy] == 1:
                break
            dy -= 1
    return dy


def compute_dy(y: int, walls_horizontal: list[list[int]], current_dir: int) -> int:
    VIEW_SIZE = 8

    if current_dir == 0:  # up
        dy = 1 if walls_horizontal[VIEW_SIZE][VIEW_SIZE + 1] == 0 else 0
    else:  # current_dir == 1 -> down
        dy = -1 if walls_horizontal[VIEW_SIZE][VIEW_SIZE] == 0 else 0
    return dy


def carnegie_wall_following(x: int, y: int, walls_horizontal: list[list[int]], clock_times: list[int]) -> tuple[int, int]:
    MAZE_SIZE = 32
    VIEW_SIZE = 8

    if x == MAZE_SIZE - 1:  # check if we can reach the end in this next move, just in case
        dy = 0
        while dy < 7:
            if walls_horizontal[VIEW_SIZE][VIEW_SIZE + dy + 1] == 1:
                break
            dy += 1
        if y + dy == MAZE_SIZE - 1:
            return dy, 5

    if clock_times[-1] == 0:
        current_dir = 0  # start going up
        try_both_sides = 0
    else:
        current_dir = (clock_times[-1] - 5) & 1  # 0 -> up, 1 -> down
        try_both_sides = ((clock_times[-1] - 5) >> 1) ^ 1
    assert 0 <= current_dir <= 1 and 0 <= try_both_sides <= 1,\
        f"current_dir={current_dir}, try_both_sides={try_both_sides}, clock_times[-1]={clock_times[-1]}"

    # if we're at the edge of the maze, we don't need to try and turn each time
    if x == 0 and current_dir == 0:  # up
        dy = carnegie_greedy(y, walls_horizontal, current_dir)
        return dy, (2 | (abs(dy) == 7)) + 5  # if we've hit a wall, turn right immediately

    if x == MAZE_SIZE - 1 and current_dir == 1:  # down
        dy = carnegie_greedy(y, walls_horizontal, current_dir)
        return dy, (2 | (abs(dy) < 7)) + 5  # if we've hit a wall, turn left immediately

    dy = compute_dy(y, walls_horizontal, current_dir)

    if dy == 0 and try_both_sides:
        current_dir ^= 1  # we know mellon's blocked, so we turn all the way around
        dy = compute_dy(y, walls_horizontal, current_dir)

    next_dir = current_dir if dy == 0 else current_dir ^ 1
    blocked = (walls_horizontal[VIEW_SIZE][VIEW_SIZE + dy + 1] if current_dir == 0 else walls_horizontal[VIEW_SIZE][VIEW_SIZE + dy]) ^ 1
    return dy, ((blocked << 1) | next_dir) + 5
