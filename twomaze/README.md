# twomaze

## Problem summary
We need to navigate a robot through a maze.
The robot has two programs: one that moves up/down and sees only walls that block up/down movement and a similar one for left/right movement.
The two programs are pure functions and can only communicate/store things in memory by adding to a clock value.
Each move also requires incrementing the clock by 5.
The goal is to reach the end while minimizing the final clock value.

There are three categories (or "patterns", as the problem calls them) of mazes.
Pattern 1 has randomly generated walls with each location having a 20% chance of having a wall.
Pattern 2 is similar, but with a 30% chance for each wall location.
Pattern 3 is an acyclic maze generated with DFS.

## Solutions
Our overall solutions focus on minimizing the amount that the clock needs to be incremented per turn.
Although the robot takes an inefficient path through the maze, the overall cost is cheap.

Our solution for pattern 3 involves following the left wall until reaching the end.
This can be implemented with a very low clock cost: each move only requires possibly sending a single bit.

For patterns 1 and 2, the solution greedily goes up and right, backtracking cell-by-cell if it gets stuck and can't move.
Once it reaches either far wall of the maze (x=31 or y=31), it starts following the wall.

Submitted code is stored in the [`submission`](/twomaze/submission) folder.
This code has a lot of duplicate functions and constants between the two files since I'm not sure if we're allowed to import between files or have *any* global variables at all, even if they're constant.
The n<sup>th</sup> submission is in `[n]_carnegie.py` and `[n]_mellon.py`, except for the first submission, which wasn't saved.

## Results
First submission: `1435234 (14650, 20287, 108587)`

Second submission: `125297 (14317, 20105, 90875)`
```
python3 main.py -p 1 -n 10000
10000 runs: mean=1306.2667, stddev=505.1118, stderr=5.0511. Took 50.7334s.

python3 main.py -p 2 -n 5000
5000 runs: mean=1968.7766, stddev=873.1762, stderr=12.3486. Took 68.8361s.

python3 main.py -p 3 -n 500
500 runs: mean=9091.428, stddev=3960.4444, stderr=177.1165. Took 72.5968s.
```

Third submission: `121519 (13003, 17641, 90875)`
```
python3 main.py -p 1 -n 10000
10000 runs: mean=1160.9801, stddev=511.9006, stderr=5.119. Took 51.3249s.

python3 main.py -p 2 -n 5000
5000 runs: mean=1669.3522, stddev=772.4428, stderr=10.924. Took 67.8052s.

python3 main.py -p 3 -n 500
500 runs: mean=9291.52, stddev=4023.973, stderr=179.9575. Took 71.6458s.
```

Fourth submission: `116562 (12603, 16558, 87401)`
```
python3 main.py -p 1 -n 10000
10000 runs: mean=1144.6213, stddev=474.6409, stderr=4.7464. Took 46.8482s.

python3 main.py -p 2 -n 5000
5000 runs: mean=1595.5528, stddev=684.1512, stderr=9.6754. Took 65.1785s.

python3 main.py -p 3 -n 500
500 runs: mean=8803.026, stddev=3962.0794, stderr=177.1896. Took 100.4248s.
```
