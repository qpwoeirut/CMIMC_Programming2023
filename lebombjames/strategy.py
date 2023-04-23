import random

BOARD_SIZE = 10
PLACEMENTS = 3


"""
#....#...x
...#....#.
.#....#...
....#....#
..#....#..
#....#....
...#....#.
.#....#...
....#....#
x.#....#..
"""


locations = [(r, c) for r in range(BOARD_SIZE) for c in range((r * 3) % 5, BOARD_SIZE, 5)]
round_num = 0
bomb_count = [0 for loc in locations]
old_board_sums = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]


def flexible_offset_pattern_strategy(pid: int, board: list[list[list[int]]]) -> list[tuple[int, int]]:
    global round_num, old_board_sums
    round_num += 1
    if round_num >= 100:
        for i, loc in enumerate(locations):
            if sum(board[loc[0]][loc[1]]) == 0:
                if old_board_sums[loc[0]][loc[1]] > 0:
                    # weight more recent rounds more heavily, in case others switch strategy
                    # assume people will probably switch at even multiple of 50
                    bomb_count[i] += 1.1 ** (round_num // 50)
                elif len([nloc for nloc in nearby_locations(loc[0], loc[1]) if sum(board[nloc[0]][nloc[1]]) == 0]) >= 2:
                    # check that at least one nearby location is also empty
                    # it's possible that a bunch of ppl place there and it was immediately blown up
                    bomb_count[i] += 0.4 * 1.1 ** (round_num // 50)

    old_board_sums = [[sum(board[r][c]) for c in range(BOARD_SIZE)] for r in range(BOARD_SIZE)]

    to_place = []
    for _ in range(3):
        to_place.append(min(locations, key=lambda loc: flexible_pattern_score(pid, board, loc)))
        board[to_place[-1][0]][to_place[-1][1]][pid] += 1
    return (to_place + [random_location() for _ in range(3)])[:3]


def flexible_pattern_score(pid: int, board: list[list[list[int]]], loc: tuple[int, int]) -> int:
    idx = locations.index(loc)
    bomb_percent = round(bomb_count[idx] * 100 / (sum(bomb_count) + 10))
    return 10 * (10 * (board[loc[0]][loc[1]][pid] * 5 + bomb_percent) + nearby_blast_score(board, loc[0], loc[1])) + random.randint(0, 9)


# counts settlements within blast radius of bomb centered at (r, c)
def blast_score(board: list[list[list[int]]], r: int, c: int) -> int:
    score = 0
    for loc in nearby_locations(r, c):
        score += sum(board[loc[0]][loc[1]])
    return score


def nearby_blast_score(board: list[list[list[int]]], r: int, c: int) -> int:
    score = 0
    for loc in nearby_locations(r, c):
        score = max(score, blast_score(board, loc[0], loc[1]))
    return score


# returns locations within blast centered at (r, c), including (r, c)
def nearby_locations(r: int, c: int) -> list[tuple[int, int]]:
    locations = [(r, c)]
    if in_board(r - 1, c):
        locations.append((r - 1, c))
    if in_board(r + 1, c):
        locations.append((r + 1, c))
    if in_board(r, c - 1):
        locations.append((r, c - 1))
    if in_board(r, c + 1):
        locations.append((r, c + 1))
    return locations


def in_board(r: int, c: int) -> bool:
    return 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE


def random_location() -> tuple[int, int]:
    return random.randint(0, BOARD_SIZE - 1), random.randint(0, BOARD_SIZE - 1)


def random_strategy(pid, board) -> list[tuple[int, int]]:
    return [random_location() for _ in range(3)]


def bad_random_strategy(pid, board) -> list[tuple[int, int]]:
    options = [
        0, 0, 0, 0, 0,
        1, 1, 1, 1,
        2, 2, 2,
        3, 3,
        4, 5, 6, 7, 8, 9
    ]
    return [(random.choice(options), random.choice(options)) for _ in range(3)]


def get_strategies():
    """
    Returns a list of strategy functions to use in a game.

    In the local tester, all of the strategies will be used as separate players in the game.
    Results will be printed out in the order of the list.

    In the official grader, only the first element of the list will be used as your strategy.
    """
    strategies = [flexible_offset_pattern_strategy] + [random_strategy for _ in range(4)]

    return strategies
