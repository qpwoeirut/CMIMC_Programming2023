def pack_move(move: int, stuck: int) -> int:
    move_val = abs(move)
    move_sign = 1 if move < 0 else 0
    return (move_val << 2) | (move_sign << 1) | stuck


def unpack_move(val: int) -> tuple[int, int]:
    if val < 0:  # first move
        return 0, 0
    stuck      = val & 0b00001
    move_sign = (val & 0b00010) >> 1
    move     = ((val & 0b11100) >> 2) * (-1 if move_sign else 1)
    return move, stuck


def calculate_visited(movements: list[str]) -> tuple[set[tuple[int, int]], set[tuple[int, int]]]:
    carnegie_visited = set()
    mellon_visited = set()

    x, y = 0, 0
    for movement in movements:
        if movement == 'L':
            mellon_visited.add((x, y))
            x -= 1
        elif movement == 'R':
            carnegie_visited.add((x, y))
            x += 1
        elif movement == 'D':
            carnegie_visited.add((x, y))
            y -= 1
        elif movement == 'U':
            carnegie_visited.add((x, y))
            y += 1
    return carnegie_visited, mellon_visited


def calculate_movements(clock_times: list[int]) -> tuple[list[str], list[str]]:
    CARNEGIE_MOVES = "DU"
    MELLON_MOVES = "LR"
    moves = [unpack_move(clock - 5)[0] for clock in clock_times]
    movements = []
    raw_movements = []
    for i, move in enumerate(moves):
        move_str = MELLON_MOVES if i % 2 == 0 else CARNEGIE_MOVES
        for _ in range(abs(move)):
            if move >= 0:
                movements.append(move_str[1])
                raw_movements.append(move_str[1])
            else:
                assert movements[-1] == move_str[1], "we should only be backtracking"
                movements.pop()
                raw_movements.append(move_str[0])
    assert set(movements) <= {'U', 'R'}, "moves should have canceled"
    return movements, raw_movements


def mellon_1(x: int, y: int, walls_vertical: list[list[int]], clock_times: list[int]) -> tuple[int, int]:
    MELLON_MOVES = "LR"
    MAZE_SIZE = 32
    VIEW_SIZE = 8

    WALL_FOLLOW_SIGNAL = 1 << 5 + 5
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

    if carnegie_stuck and mellon_stuck:  # stuck mode
        dx = -1 if movements[-1] in MELLON_MOVES else 0
    return dx, pack_move(dx, mellon_stuck) + 5


def mellon_2(x: int, y: int, walls_vertical: list[list[int]], clock_times: list[int]) -> tuple[int, int]:
    return mellon_1(x, y, walls_vertical, clock_times)


def mellon_3(x: int, y: int, walls_vertical: list[list[int]], clock_times: list[int]) -> tuple[int, int]:
    return mellon_wall_following(x, y, walls_vertical, clock_times, right_wall=0)


def mellon_wall_following(x: int, y: int, walls_vertical: list[list[int]], clock_times: list[int], right_wall: int) -> tuple[int, int]:
    MAZE_SIZE = 32
    VIEW_SIZE = 8

    WALL_FOLLOW_SIGNAL = 1 << 5 + 5

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

    if current_dir == 0:  # right
        dx = 1 if x + 1 < MAZE_SIZE and walls_vertical[VIEW_SIZE + 1][VIEW_SIZE] == 0 else 0
    elif current_dir == 1:  # left
        dx = -1 if x > 0 and walls_vertical[VIEW_SIZE][VIEW_SIZE] == 0 else 0
    else:
        raise ValueError(f"current_dir={current_dir}, clock_times[-1]={clock_times[-1]}")

    next_dir = (current_dir ^ 1 if dx == 0 else current_dir) ^ right_wall
    return dx, next_dir + 5
