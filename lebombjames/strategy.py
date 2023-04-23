import random
from typing import Callable

BOARD_SIZE = 10
PLACEMENTS = 3

"""
#..#..#..#
.x......x.
..........
#..#..#..#
x........x
..........
#..#..#..#
x........x
..........
#..#..#..#
"""
def grid_pattern_strategy(pid: int, board: list[list[list[int]]]) -> list[tuple[int, int]]:
    locations = [(r, c) for r in range(0, 3, BOARD_SIZE) for c in range(0, 3, BOARD_SIZE)]
    return pattern_strategy(pid, board, locations)


"""
#....#....
...#....#.
.#....#...
....#....#
..#....#..
#....#....
...#....#.
.#....#...
....#....#
..#....#..
"""
def offset_pattern_strategy(pid: int, board: list[list[list[int]]]) -> list[tuple[int, int]]:
    locations = [(r, c) for r in range(BOARD_SIZE) for c in range((r * 3) % 5, BOARD_SIZE, 5)]
    return pattern_strategy(pid, board, locations)


"""
#...#...##
..#...#...
..........
#...#...#.
..#...#...
..........
#...#...#.
..#...#...
..........
#...#...##
"""
def two_row_pattern_strategy(pid: int, board: list[list[list[int]]]) -> list[tuple[int, int]]:
    locations = [(r, c) for r in range(BOARD_SIZE) for c in range((r * 3) % 5, BOARD_SIZE, 5)]
    return pattern_strategy(pid, board, locations)


def pattern_strategy(pid: int, board: list[list[list[int]]], pattern_locations: list[tuple[int, int]]) -> list[tuple[int, int]]:
    primary = [loc for loc in pattern_locations if board[loc[0]][loc[1]][pid] == 0]
    secondary = [loc for loc in pattern_locations if board[loc[0]][loc[1]][pid] == 1]
    primary.sort(key=lambda loc: nearby_blast_score(board, loc[0], loc[1]))
    secondary.sort(key=lambda loc: nearby_blast_score(board, loc[0], loc[1]))
    return (primary + secondary + [random_location() for _ in range(3)])[:3]


def lurking_score(board: list[list[list[int]]], r: int, c: int) -> int:
    score = blast_score(board, r, c) * 100
    if in_board(r - 2, c - 2):
        score -= sum(board[r - 2][c - 2])
    if in_board(r - 2, c + 2):
        score -= sum(board[r - 2][c + 2])
    if in_board(r + 2, c - 2):
        score -= sum(board[r + 2][c - 2])
    if in_board(r + 2, c + 2):
        score -= sum(board[r + 2][c + 2])
    return score


def lurking_strategy(pid: int, board: list[list[list[int]]]) -> list[tuple[int, int]]:
    return minimum_score(pid, board, lurking_score)


def random_lurking_strategy(pid: int, board: list[list[list[int]]]) -> list[tuple[int, int]]:
    return random_minimum_score(pid, board, lurking_score)


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


def random_distancing_strategy(pid: int, board: list[list[list[int]]]) -> list[tuple[int, int]]:
    return random_minimum_score(pid, board, blast_score)


def distancing_strategy(pid: int, board: list[list[list[int]]]) -> list[tuple[int, int]]:
    return minimum_score(pid, board, blast_score)


def random_minimum_score(pid: int, board: list[list[list[int]]], score_func: Callable[[[list[list[list[int]]]], int, int], int]) -> list[
    tuple[int, int]]:
    to_place = []

    scores = [[0 for _ in row] for row in board]
    for _ in range(PLACEMENTS):
        min_score = float("inf")
        min_locs = []
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                scores[r][c] = score_func(board, r, c)
                if min_score > scores[r][c]:
                    min_score = scores[r][c]
                    min_locs = []
                if min_score == scores[r][c]:
                    min_locs.append((r, c))

        min_r, min_c = random.choice(min_locs)
        board[min_r][min_c][pid] += 1
        to_place.append((min_r, min_c))
    return to_place


def minimum_score(pid: int, board: list[list[list[int]]], score_func: Callable[[[list[list[list[int]]]], int, int], int]) -> list[tuple[int, int]]:
    to_place = []

    scores = [[0 for _ in row] for row in board]
    for _ in range(PLACEMENTS):
        min_score = float("inf")
        min_r, min_c = 0, 0
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                scores[r][c] = score_func(board, r, c)
                if min_score > scores[r][c]:
                    min_score = scores[r][c]
                    min_r = r
                    min_c = c
        board[min_r][min_c][pid] += 1
        to_place.append((min_r, min_c))
    return to_place


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
    return random.randint(0, 9), random.randint(0, 9)


def random_strategy(pid, board) -> list[tuple[int, int]]:
    return [random_location() for _ in range(3)]


def random_border_location() -> tuple[int, int]:
    edge_value = random.randint(0, 1) * 9
    if random.randint(0, 1) == 0:
        return edge_value, random.randint(0, 9)
    else:
        return random.randint(0, 9), edge_value


def random_border_strategy(pid, board) -> list[tuple[int, int]]:
    return [random_border_location() for _ in range(3)]


def random_corner_strategy(pid, board) -> list[tuple[int, int]]:
    return [(random.randint(0, 1) * 9, random.randint(0, 1) * 9) for _ in range(PLACEMENTS)]


def get_strategies():
    """
    Returns a list of strategy functions to use in a game.

    In the local tester, all of the strategies will be used as separate players in the game.
    Results will be printed out in the order of the list.

    In the official grader, only the first element of the list will be used as your strategy. 
    """
    strategies = [offset_pattern_strategy, grid_pattern_strategy, lurking_strategy, random_strategy, random_border_strategy]

    return strategies


def main():
    from lebombjames.grader import LebombJamesGrader
    grader = LebombJamesGrader(True, False)
    grader.grade()
    grader.print_result()


if __name__ == "__main__":
    main()
