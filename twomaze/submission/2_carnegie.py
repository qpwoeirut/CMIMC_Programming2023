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


def carnegie_1(x: int, y: int, walls_horizontal: list[list[int]], clock_times: list[int]) -> tuple[int, int]:
    CARNEGIE_MOVES = "DU"
    MAZE_SIZE = 32
    VIEW_SIZE = 8

    WALL_FOLLOW_SIGNAL = 1 << 5 + 5
    max_clock = max(clock_times)
    if max_clock >= WALL_FOLLOW_SIGNAL:
        return carnegie_wall_following(x, y, walls_horizontal, clock_times, right_wall=max_clock & 1)

    if y == MAZE_SIZE - 1:
        return 0, WALL_FOLLOW_SIGNAL

    if x == 0 and y == 0 and len(clock_times) >= 5:  # all the backtracking ended up with us at the start again >:(
        return 0, WALL_FOLLOW_SIGNAL  # run wall following as a fallback; it'll get to the end eventually


    movements, raw_movements = calculate_movements(clock_times)
    carnegie_visited, mellon_visited = calculate_visited(raw_movements)

    _, mellon_stuck = unpack_move(clock_times[-1] - 5)
    dy = 0
    carnegie_stuck = 1
    if (x, y + 1) not in carnegie_visited:
        carnegie_stuck = 0
        while y + dy < MAZE_SIZE - 1 and dy < 7:
            if walls_horizontal[VIEW_SIZE][VIEW_SIZE + dy + 1] == 1:
                carnegie_stuck = 1
                break
            dy += 1
            mellon_stuck = 0  # once we start moving, we don't know if mellon is stuck anymore

    if carnegie_stuck and mellon_stuck:  # stuck mode
        dy = -1 if movements[-1] in CARNEGIE_MOVES else 0
    return dy, pack_move(dy, carnegie_stuck) + 5


def carnegie_2(x: int, y: int, walls_horizontal: list[list[int]], clock_times: list[int]) -> tuple[int, int]:
    return carnegie_1(x, y, walls_horizontal, clock_times)  # idk hopefully it works okay


# classic wall-following strategy for mazes. maintain the direction we're going in and always turn left if possible
def carnegie_3(x: int, y: int, walls_horizontal: list[list[int]], clock_times: list[int]) -> tuple[int, int]:
    return carnegie_wall_following(x, y, walls_horizontal, clock_times, right_wall=0)


def carnegie_wall_following(x: int, y: int, walls_horizontal: list[list[int]], clock_times: list[int], right_wall: int) -> tuple[int, int]:
    MAZE_SIZE = 32
    VIEW_SIZE = 8

    WALL_FOLLOW_SIGNAL = 1 << 5 + 5

    if x == MAZE_SIZE - 1:  # check if we can reach the end in this next move, just in case
        dy = 0
        while y + dy < MAZE_SIZE - 1 and dy < 7:
            if walls_horizontal[VIEW_SIZE][VIEW_SIZE + dy + 1] == 1:
                break
            dy += 1
        if y + dy == MAZE_SIZE - 1:
            return dy, 5


    if clock_times[-1] == 0 or clock_times[-1] >= WALL_FOLLOW_SIGNAL:
        current_dir = 0  # start going up
    else:
        current_dir = clock_times[-1] - 5  # 0 -> up, 1 -> down

    if current_dir == 0:  # up
        dy = 1 if y + 1 < MAZE_SIZE and walls_horizontal[VIEW_SIZE][VIEW_SIZE + 1] == 0 else 0
    elif current_dir == 1:  # down
        dy = -1 if y > 0 and walls_horizontal[VIEW_SIZE][VIEW_SIZE] == 0 else 0
    else:
        raise ValueError(f"current_dir={current_dir}, clock_times[-1]={clock_times[-1]}")

    next_dir = (current_dir if dy == 0 else current_dir ^ 1) ^ right_wall
    return dy, next_dir + 5
