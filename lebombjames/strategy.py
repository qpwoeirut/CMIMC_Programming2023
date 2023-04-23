"""
Edit this file! This is the file you will submit.
"""
import random

BOARD_SIZE = 10
PLACEMENTS = 3


def distancing_strategy(pid, board):
    to_place = []

    scores = [[0 for _ in row] for row in board]
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            scores[r][c] = blast_score(board, r, c)

    for _ in range(PLACEMENTS):
        min_score = float("inf")
        min_r, min_c = 0, 0
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if min_score > scores[r][c]:
                    min_score = scores[r][c]
                    min_r = r
                    min_c = c
        for loc in nearby_locations(min_r, min_c):
            scores[loc[0]][loc[1]] += 1
        to_place.append((min_r, min_c))
    return to_place


# counts settlements within blast radius of bomb centered at (r, c)
def blast_score(board, r, c) -> int:
    score = 0
    for loc in nearby_locations(r, c):
        score += sum(board[loc[0]][loc[1]])
    return score


# returns locations within blast centered at (r, c), including (r, c)
def nearby_locations(r: int, c: int) -> list[tuple[int, int]]:
    locations = [(r, c)]
    if r > 0:
        locations.append((r - 1, c))
    if r + 1 < BOARD_SIZE:
        locations.append((r + 1, c))
    if c > 0:
        locations.append((r, c - 1))
    if c + 1 < BOARD_SIZE:
        locations.append((r, c + 1))
    return locations


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


def random_border(pid, board) -> list[tuple[int, int]]:
    return [random_border_location() for _ in range(3)]


def get_strategies():
    """
    Returns a list of strategy functions to use in a game.

    In the local tester, all of the strategies will be used as separate players in the game.
    Results will be printed out in the order of the list.

    In the official grader, only the first element of the list will be used as your strategy. 
    """
    strategies = [distancing_strategy, random_strategy, random_strategy, random_border, random_border]

    return strategies


def main():
    from lebombjames.grader import LebombJamesGrader
    grader = LebombJamesGrader(True, False)
    grader.grade()
    grader.print_result()


if __name__ == "__main__":
    main()