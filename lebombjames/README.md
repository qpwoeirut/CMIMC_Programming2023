# Lebomb James
by qpwoeirut

## Problem summary
We're in a 5-player game where we place 3 settlements per round in a 10x10 grid.
After each round, two cross shapes of size 5 are "bombed" and all settlements in those squares are removed.
The bombing sites are chosen such that the amount of settlements destroyed is maximized.

There are 1000 rounds total.
Our goal is to maximize the amount of settlements we have at the end of each round **for the last 100 rounds only**.


## Overall Approach
We initially didn't spend much time on Lebomb.
My two teammates were working on L3 and Auction, and I was working on Twomaze.
Working on Lebomb was my way of taking a break from Twomaze, and my goal was to get a simple solution that would be easy to implement.

Our team approached both AI problems by writing all the simple strategies we could think of, in order to see how they'd stack up against each other.
Since both problems/games are influenced by opponent behavior, it's important to test your solution against the solutions that other teams may have come up with.
I started by writing a couple randomized solutions and then worked on more sophisticated ideas.
All strategies are in either [old_strategy.py](/lebombjames/old_strategy.py) or [strategy.py](/lebombjames/strategy.py).
The solutions are described below.

### random_strategy, random_border_strategy, random_corner_strategy
These pick a random location in the board, on the border, or in a corner, respectively.
As you might expect, these strategies do rather poorly.

### distancing_strategy, random_distancing_strategy
The first strategy I came up with was to place settlements in locations that were not likely to be bombed.
This strategy scores a location by summing the amount of settlements that would be destroyed by a bomb at that spot.

### lurking_strategy, random_lurking_strategy
This strategy places near large groups of settlements.
The intuition is that those groups of settlements will get bombed, and then the settlement we just placed won't have as many neighbors and will therefore survive for longer.

### pattern_strategy (offset_pattern_strategy, grid_pattern_strategy, two_row_pattern_strategy)
My next idea was to lay out our settlements such that each bomb can only take out one of our settlements.
Since two bombs are dropped per round, at most two of our settlements will need replacing.
I wrote three different patterns. The best one (offset) is shown below.
```
Offset (20 locations):
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
```

The offset pattern guarantees that we can have at least 18 settlements on the board at the end of each round, since we'll be able to place in 20 locations and at most 2 will be bombed.
If any locations are empty, we'll build there.
Once each location has a settlement, we'll start stacking on the same locations.
At the time, I thought this would always be more optimal than building at a new location because it would minimize the places that a bomb could be dropped and destroy two of our settlements, but, in hindsight, I don't think that's true.

## Final Solution
Our final solution involved using the offset pattern strategy (described above) with some heuristics for picking which location to build in.

The final solution code is below.
`nearby_locations` returns the 5 locations that would be affected if a bomb was dropped at the given spot.
`nearby_blast_score` calculates the destruction caused by a bomb dropped in any nearby location and returns the maximum of those values.
```python
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
```

In order to take into account the strategies of our opponents, I tried to track which of our locations were bombed often.
The amount of times a location was bombed is stored in `bomb_count`.
Since other players may change strategies late in the game, more recent events have a higher weight.

The `flexible_pattern_score` is used to pick which location we'll build in.
The amount of settlements we currently have at a location is the largest factor, but I weighted that value so that a location that gets bombed very often won't be built upon very often.
`nearby_blast_score` is included to try and avoid building in locations that will be immediately bombed.


## Other Strategies
My team and I discussed writing a strategy that would intentionally sabotage other teams by trying to draw bombs towards them, but we never got around to implementing it.
The sabotage strategy is incompatible with the pattern strategy anyway, since one of your settlements will get hit no matter where the bomb goes.