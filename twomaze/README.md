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

Submitted code is stored in [`carnegie.py`](/twomaze/carnegie.py) and [`mellon.py`](/twomaze/mellon.py).
This code has a lot of duplicate functions and constants between the two files since I'm not sure if we're allowed to import between files or have *any* global variables at all, even if they're constant.
The solution code for editing is in the [`working_solutions`](/twomaze/working_solutions) folder.

## Local results
```
python3 main.py -p 1 -n 1000
Average across 1000 runs: 1333.861

python3 main.py -p 2 -n 1000
Average across 1000 runs: 1991.536

python3 main.py -p 3 -n 100 
Average across 100 runs: 10068.09
```