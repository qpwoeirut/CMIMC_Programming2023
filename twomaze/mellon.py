from carnegie import *


def mellon_1(x: int, y: int, walls_vertical: list[list[int]], clock_times: list[int]) -> tuple[int, int]:
    max_clock = max(clock_times)
    if max_clock >= WALL_FOLLOW_SIGNAL:
        return mellon_wall_following(x, y, walls_vertical, clock_times, right_wall=max_clock & 1)

    if x == MAZE_SIZE - 1:
        return 0, WALL_FOLLOW_SIGNAL + 1  # add 1 to signal right-wall following, not left-wall following

    movements = calculate_movements(clock_times)
    _, mellon_visited = calculate_visited(movements)

    dx = 0
    if (x + 1, y) not in mellon_visited:
        dx = mellon_greedy(y, walls_vertical, 0)
    if dx == 0 and mellon_greedy(y, walls_vertical, 1) <= -1:
        dx = -1

    return dx, (dx + 1) + 5


def mellon_2(x: int, y: int, walls_vertical: list[list[int]], clock_times: list[int]) -> tuple[int, int]:
    return mellon_wall_following(x, y, walls_vertical, clock_times, right_wall=0)


def mellon_3(x: int, y: int, walls_vertical: list[list[int]], clock_times: list[int]) -> tuple[int, int]:
    return mellon_wall_following(x, y, walls_vertical, clock_times, right_wall=0)


def mellon_greedy(x: int, walls_vertical: list[list[int]], current_dir: int) -> int:
    dx = 0
    if current_dir == 0:  # right
        while dx < 7:
            if walls_vertical[VIEW_SIZE + dx + 1][VIEW_SIZE] == 1:
                break
            dx += 1
    else:  # left
        while dx > -7:
            if walls_vertical[VIEW_SIZE + dx][VIEW_SIZE] == 1:
                break
            dx -= 1
    return dx


def compute_dx(x: int, walls_vertical: list[list[int]], current_dir: int) -> int:
    if current_dir == 0:  # right
        dx = 1 if walls_vertical[VIEW_SIZE + 1][VIEW_SIZE] == 0 else 0
    else:  # current_dir == 1 -> left
        dx = -1 if walls_vertical[VIEW_SIZE][VIEW_SIZE] == 0 else 0
    return dx


def mellon_wall_following(x: int, y: int, walls_vertical: list[list[int]], clock_times: list[int], right_wall: int) -> tuple[int, int]:
    if y == MAZE_SIZE - 1:  # check if we can reach the end in this next move, just in case
        dx = 0
        while dx < 7:
            if walls_vertical[VIEW_SIZE + dx + 1][VIEW_SIZE] == 1:
                break
            dx += 1
        if x + dx == MAZE_SIZE - 1:
            return dx, 5

    if clock_times[-1] == 0 or clock_times[-1] >= WALL_FOLLOW_SIGNAL:
        current_dir = 0  # start going right
        try_both_sides = 0
    else:
        current_dir = (clock_times[-1] - 5) & 1  # 0 -> right, 1 -> left
        try_both_sides = ((clock_times[-1] - 5) >> 1) ^ 1
    assert 0 <= current_dir <= 1 and 0 <= try_both_sides <= 1,\
        f"current_dir={current_dir}, try_both_sides={try_both_sides}, clock_times[-1]={clock_times[-1]}"

    # if we're at the edge of the maze, we don't need to try and turn each time
    if y == 0 and current_dir ^ right_wall == 1:  # left + left wall or right + right wall
        dx = mellon_greedy(x, walls_vertical, current_dir)
        return dx, (2 | (abs(dx) == 7)) + 5  # if we've hit a wall, turn up immediately

    if y == MAZE_SIZE - 1 and current_dir ^ right_wall == 0:
        dx = mellon_greedy(x, walls_vertical, current_dir)
        return dx, (2 | (abs(dx) < 7)) + 5  # if we've hit a wall, turn down immediately

    dx = compute_dx(x, walls_vertical, current_dir)

    if dx == 0 and try_both_sides:
        current_dir ^= 1  # we know carnegie's blocked, so we turn all the way around
        dx = compute_dx(x, walls_vertical, current_dir)

    next_dir = (current_dir ^ 1 if dx == 0 else current_dir) ^ right_wall
    blocked = (walls_vertical[VIEW_SIZE + dx + 1][VIEW_SIZE] if current_dir == 0 else walls_vertical[VIEW_SIZE + dx][VIEW_SIZE]) ^ 1
    return dx, ((blocked << 1) | next_dir) + 5
