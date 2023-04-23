from carnegie import *


def mellon_1(x: int, y: int, walls_vertical: list[list[int]], clock_times: list[int]) -> tuple[int, int]:
    max_clock = max(clock_times)
    if max_clock >= WALL_FOLLOW_SIGNAL:
        return mellon_wall_following(x, y, walls_vertical, clock_times, right_wall=max_clock & 1)

    if x == MAZE_SIZE - 1:
        return 0, WALL_FOLLOW_SIGNAL + 1  # add 1 to signal right-wall following, not left-wall following

    if x == 0 and y == 0 and len(clock_times) >= 5:  # all the backtracking ended up with us at the start again >:(
        return 0, WALL_FOLLOW_SIGNAL  # run wall following as a fallback; it'll get to the end eventually

    movements, raw_movements = calculate_movements(clock_times)
    carnegie_visited, mellon_visited = calculate_visited(raw_movements)

    _, carnegie_stuck = unpack_move(clock_times[-1] - 5)
    dx = 0
    mellon_stuck = 1
    if (x + 1, y) not in mellon_visited:
        mellon_stuck = 0
        while x + dx < MAZE_SIZE - 1 and dx < 7:
            if walls_vertical[VIEW_SIZE + dx + 1][VIEW_SIZE] == 1:
                mellon_stuck = 1
                break
            dx += 1
            carnegie_stuck = 0  # once we start moving, we don't know if carnegie is stuck anymore
        mellon_stuck |= x + dx + 1 == MAZE_SIZE

    if carnegie_stuck and mellon_stuck:  # stuck mode
        dx = -1 if movements[-1] in MELLON_MOVES else 0
    return dx, pack_move(dx, mellon_stuck) + 5


def mellon_2(x: int, y: int, walls_vertical: list[list[int]], clock_times: list[int]) -> tuple[int, int]:
    return mellon_1(x, y, walls_vertical, clock_times)


def mellon_3(x: int, y: int, walls_vertical: list[list[int]], clock_times: list[int]) -> tuple[int, int]:
    return mellon_wall_following(x, y, walls_vertical, clock_times, right_wall=0)


def mellon_greedy(x: int, walls_vertical: list[list[int]], current_dir: int) -> int:
    dx = 0
    if current_dir == 0:  # right
        while x + dx < MAZE_SIZE - 1 and dx < 7:
            if walls_vertical[VIEW_SIZE + dx + 1][VIEW_SIZE] == 1:
                break
            dx += 1
    else:  # left
        while x + dx > 0 and dx > -7:
            if walls_vertical[VIEW_SIZE + dx][VIEW_SIZE] == 1:
                break
            dx -= 1
    return dx


def mellon_wall_following(x: int, y: int, walls_vertical: list[list[int]], clock_times: list[int], right_wall: int) -> tuple[int, int]:
    if y == MAZE_SIZE - 1:  # check if we can reach the end in this next move, just in case
        dx = 0
        while x + dx < MAZE_SIZE - 1 and dx < 7:
            if walls_vertical[VIEW_SIZE + dx + 1][VIEW_SIZE] == 1:
                break
            dx += 1
        if x + dx == MAZE_SIZE - 1:
            return dx, 5


    if clock_times[-1] < 5 or clock_times[-1] >= WALL_FOLLOW_SIGNAL:
        current_dir = 0  # start going right
    else:
        current_dir = clock_times[-1] - 5  # 0 -> right, 1 -> left
    assert 0 <= current_dir <= 1, f"current_dir={current_dir}, clock_times[-1]={clock_times[-1]}"

    # if we're at the edge of the maze, we don't need to try and turn each time
    if y == 0 and current_dir ^ right_wall == 1:  # left + left wall or right + right wall
        dx = mellon_greedy(x, walls_vertical, current_dir)
        if dx != 0:
            return dx, (abs(dx) == 7) + 5  # if we've hit a wall, turn right immediately

    if y == MAZE_SIZE - 1 and current_dir ^ right_wall == 0:
        dx = mellon_greedy(x, walls_vertical, current_dir)
        if dx != 0:
            return dx, (abs(dx) != 7) + 5  # if we've hit a wall, turn left immediately

    if current_dir == 0:  # right
        dx = 1 if x + 1 < MAZE_SIZE and walls_vertical[VIEW_SIZE + 1][VIEW_SIZE] == 0 else 0
    else:  # current_dir == 1 -> left
        dx = -1 if x > 0 and walls_vertical[VIEW_SIZE][VIEW_SIZE] == 0 else 0

    next_dir = (current_dir ^ 1 if dx == 0 else current_dir) ^ right_wall
    return dx, next_dir + 5
