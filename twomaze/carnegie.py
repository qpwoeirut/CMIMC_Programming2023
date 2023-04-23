CARNEGIE_MOVES = "DU"
MELLON_MOVES = "LR"
MAZE_SIZE = 32
VIEW_SIZE = 8

def carnegie_1(x: int, y: int, walls_horizontal: list[list[int]], clock_times: list[int]) -> tuple[int, int]:
    return carnegie_wall_following(x, y, walls_horizontal, clock_times)


def carnegie_2(x: int, y: int, walls_horizontal: list[list[int]], clock_times: list[int]) -> tuple[int, int]:
    return carnegie_1(x, y, walls_horizontal, clock_times)  # idk hopefully it works okay


# classic wall-following strategy for mazes. maintain the direction we're going in and always turn left if possible
def carnegie_3(x: int, y: int, walls_horizontal: list[list[int]], clock_times: list[int]) -> tuple[int, int]:
    return carnegie_wall_following(x, y, walls_horizontal, clock_times)


def carnegie_greedy(y: int, walls_horizontal: list[list[int]], current_dir: int) -> int:
    dy = 0
    if current_dir == 0:  # up
        while y + dy < MAZE_SIZE - 1 and dy < 7:
            if walls_horizontal[VIEW_SIZE][VIEW_SIZE + dy + 1] == 1:
                break
            dy += 1
    else:  # down
        while y + dy > 0 and dy > -7:
            if walls_horizontal[VIEW_SIZE][VIEW_SIZE + dy] == 1:
                break
            dy -= 1
    return dy


def carnegie_wall_following(x: int, y: int, walls_horizontal: list[list[int]], clock_times: list[int]) -> tuple[int, int]:
    if x == MAZE_SIZE - 1:  # check if we can reach the end in this next move, just in case
        dy = 0
        while y + dy < MAZE_SIZE - 1 and dy < 7:
            if walls_horizontal[VIEW_SIZE][VIEW_SIZE + dy + 1] == 1:
                break
            dy += 1
        if y + dy == MAZE_SIZE - 1:
            return dy, 5


    if clock_times[-1] == 0:
        current_dir = 0  # start going up
    else:
        current_dir = clock_times[-1] - 5  # 0 -> up, 1 -> down
    assert 0 <= current_dir <= 1, f"current_dir={current_dir}, clock_times[-1]={clock_times[-1]}"

    # if we're at the edge of the maze, we don't need to try and turn each time
    if x == 0 and current_dir == 0:  # up + left wall or down + right wall
        dy = carnegie_greedy(y, walls_horizontal, current_dir)
        return dy, (abs(dy) == 7) + 5  # if we've hit a wall, turn right immediately

    if x == MAZE_SIZE - 1 and current_dir == 1:
        dy = carnegie_greedy(y, walls_horizontal, current_dir)
        return dy, (abs(dy) != 7) + 5  # if we've hit a wall, turn left immediately

    if current_dir == 0:  # up
        dy = 1 if y + 1 < MAZE_SIZE and walls_horizontal[VIEW_SIZE][VIEW_SIZE + 1] == 0 else 0
    else:  # current_dir == 1 -> down
        dy = -1 if y > 0 and walls_horizontal[VIEW_SIZE][VIEW_SIZE] == 0 else 0

    next_dir = current_dir if dy == 0 else current_dir ^ 1
    return dy, next_dir + 5


def main():
    from twomaze.grader import TwoMazeGrader
    grader = TwoMazeGrader(2, True)
    grader.grade()
    grader.print_result()


if __name__ == "__main__":
    main()
