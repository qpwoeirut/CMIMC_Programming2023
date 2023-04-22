"""
TwoMaze local tester command line interface.

Usage:
    python3 main.py [-d] [-p <pattern>] [--help]
"""

import argparse
from grader import TwoMazeGrader

parser = argparse.ArgumentParser(description="TwoMaze local runner CLI")

parser.add_argument("--debug", "-d", action="store_true")
parser.add_argument("--pattern", "-p", type=int, default=1)
parser.add_argument("--count", "-n", type=int, default=1)

args = parser.parse_args()

graders = []
for _ in range(args.count):
    grader = TwoMazeGrader(args.pattern, args.debug)
    grader.grade()
    graders.append(grader)

if args.count == 1:
    graders[0].print_result()
else:
    mean = sum([grader.result for grader in graders]) / args.count
    print(f"Average across {args.count} runs: {mean}")
