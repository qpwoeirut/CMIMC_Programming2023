CARNEGIE_MOVES = "DU"
MELLON_MOVES = "LR"
MAZE_SIZE = 32
VIEW_SIZE = 8

WALL_FOLLOW_SIGNAL = 9 + 5

def calculate_visited(movements: list[str]) -> tuple[set[tuple[int, int]], set[tuple[int, int]]]:
    carnegie_visited = set()
    mellon_visited = set()

    x, y = 0, 0
    for movement in movements:
        if movement == 'L':
            mellon_visited.add((x, y))
            x -= 1
            mellon_visited.add((x, y))
        elif movement == 'R':
            mellon_visited.add((x, y))
            x += 1
            mellon_visited.add((x, y))
        elif movement == 'D':
            carnegie_visited.add((x, y))
            y -= 1
            carnegie_visited.add((x, y))
        elif movement == 'U':
            carnegie_visited.add((x, y))
            y += 1
            carnegie_visited.add((x, y))
    return carnegie_visited, mellon_visited


def calculate_movements(clock_times: list[int]) -> list[str]:
    moves = [(clock - 5) - 1 for clock in clock_times[1:]]
    raw_movements = []
    for i, move in enumerate(moves):
        move_str = CARNEGIE_MOVES if i % 2 == 0 else MELLON_MOVES
        for _ in range(abs(move)):
            if move >= 0:
                raw_movements.append(move_str[1])
            else:
                raw_movements.append(move_str[0])
    return raw_movements


# this strategy has a very good median score but also gets stuck and dies sometimes. decided not to submit it.
def carnegie_1(x: int, y: int, walls_horizontal: list[list[int]], clock_times: list[int]) -> tuple[int, int]:
    max_clock = max(clock_times)
    if max_clock >= WALL_FOLLOW_SIGNAL:
        return carnegie_wall_following(x, y, walls_horizontal, clock_times, right_wall=max_clock & 1)

    if y == MAZE_SIZE - 1:
        return 0, WALL_FOLLOW_SIGNAL

    movements = calculate_movements(clock_times)
    carnegie_visited, _ = calculate_visited(movements)

    dy = 0
    if (x, y + 1) not in carnegie_visited or (len(clock_times) >= 5 and set(clock_times) == {6}):
        dy = carnegie_greedy(y, walls_horizontal, 0)
    if dy == 0 and carnegie_greedy(y, walls_horizontal, 1) <= -1:
        dy = -1

    return dy, (dy + 1) + 5


def carnegie_2(x: int, y: int, walls_horizontal: list[list[int]], clock_times: list[int]) -> tuple[int, int]:
    return carnegie_wall_following(x, y, walls_horizontal, clock_times, right_wall=0)


# classic wall-following strategy for mazes. maintain the direction we're going in and always turn left if possible
def carnegie_3(x: int, y: int, walls_horizontal: list[list[int]], clock_times: list[int]) -> tuple[int, int]:
    return carnegie_wall_following(x, y, walls_horizontal, clock_times, right_wall=0)


def carnegie_greedy(y: int, walls_horizontal: list[list[int]], current_dir: int) -> int:
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
    if current_dir == 0:  # up
        dy = 1 if walls_horizontal[VIEW_SIZE][VIEW_SIZE + 1] == 0 else 0
    else:  # current_dir == 1 -> down
        dy = -1 if walls_horizontal[VIEW_SIZE][VIEW_SIZE] == 0 else 0
    return dy


def carnegie_wall_following(x: int, y: int, walls_horizontal: list[list[int]], clock_times: list[int], right_wall: int) -> tuple[int, int]:
    if x == MAZE_SIZE - 1:  # check if we can reach the end in this next move, just in case
        dy = 0
        while dy < 7:
            if walls_horizontal[VIEW_SIZE][VIEW_SIZE + dy + 1] == 1:
                break
            dy += 1
        if y + dy == MAZE_SIZE - 1:
            return dy, 5

    if clock_times[-1] == 0 or clock_times[-1] >= WALL_FOLLOW_SIGNAL:
        current_dir = 0  # start going up
        try_both_sides = 0
    else:
        current_dir = (clock_times[-1] - 5) & 1  # 0 -> up, 1 -> down
        try_both_sides = ((clock_times[-1] - 5) >> 1) ^ 1
    assert 0 <= current_dir <= 1 and 0 <= try_both_sides <= 1,\
        f"current_dir={current_dir}, try_both_sides={try_both_sides}, clock_times[-1]={clock_times[-1]}"

    # if we're at the edge of the maze, we don't need to try and turn each time
    if x == 0 and current_dir ^ right_wall == 0:  # up
        dy = carnegie_greedy(y, walls_horizontal, current_dir)
        return dy, (2 | (abs(dy) == 7)) + 5  # if we've hit a wall, turn right immediately

    if x == MAZE_SIZE - 1 and current_dir ^ right_wall == 1:  # down
        dy = carnegie_greedy(y, walls_horizontal, current_dir)
        return dy, (2 | (abs(dy) < 7)) + 5  # if we've hit a wall, turn left immediately

    dy = compute_dy(y, walls_horizontal, current_dir)

    if dy == 0 and try_both_sides:
        current_dir ^= 1  # we know mellon's blocked, so we turn all the way around
        dy = compute_dy(y, walls_horizontal, current_dir)

    next_dir = (current_dir if dy == 0 else current_dir ^ 1) ^ right_wall
    blocked = (walls_horizontal[VIEW_SIZE][VIEW_SIZE + dy + 1] if current_dir == 0 else walls_horizontal[VIEW_SIZE][VIEW_SIZE + dy]) ^ 1
    return dy, ((blocked << 1) | next_dir) + 5


def main():
    from twomaze.grader import TwoMazeGrader
    while True:
        grader = TwoMazeGrader(1, True)
        grader.grade()
        grader.print_result()


if __name__ == "__main__":
    main()
