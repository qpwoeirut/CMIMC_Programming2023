from typing import Callable

from lebombjames.strategy import *


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
def offset_pattern_strategy(pid: int, board: list[list[list[int]]]) -> list[tuple[int, int]]:
    locations = [(r, c) for r in range(BOARD_SIZE) for c in range((r * 3) % 5, BOARD_SIZE, 5)] + [(9, 0), (0, 9)]
    return pattern_strategy(pid, board, locations)


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
    to_place = []
    for _ in range(3):
        to_place.append(
            min(pattern_locations,
                key=lambda loc: nearby_blast_score(board, loc[0], loc[1]) + board[loc[0]][loc[1]][pid] * 3)
        )
        board[to_place[-1][0]][to_place[-1][1]][pid] += 1
    return (to_place + [random_location() for _ in range(3)])[:3]


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


def main():
    from lebombjames.grader import LebombJamesGrader
    grader = LebombJamesGrader(True, True)

    for _ in range(1):
        grader.grade()
        grader.print_result()


if __name__ == "__main__":
    main()
