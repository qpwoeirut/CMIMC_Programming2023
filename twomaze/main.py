"""
TwoMaze local tester command line interface.

Usage:
    python3 main.py [-d] [-p <pattern>] [--help]
"""

import argparse
import math
from time import time

from grader import TwoMazeGrader

parser = argparse.ArgumentParser(description="TwoMaze local runner CLI")

parser.add_argument("--debug", "-d", action="store_true")
parser.add_argument("--pattern", "-p", type=int, default=1)
parser.add_argument("--count", "-n", type=int, default=1)

args = parser.parse_args()

start_time = time()
graders = []
for _ in range(args.count):
    grader = TwoMazeGrader(args.pattern, args.debug)
    grader.grade()
    graders.append(grader)
time_taken = round(time() - start_time, 4)

if args.count == 1:
    graders[0].print_result()
else:
    mean = sum([grader.result for grader in graders]) / args.count
    stddev = math.sqrt(sum([(grader.result - mean) ** 2 for grader in graders]) / (args.count - 1))
    stderr = stddev / math.sqrt(args.count)
    print(f"{args.count} runs: mean={mean}, stddev={round(stddev, 4)}, stderr={round(stderr, 4)}. Took {time_taken}s.")
