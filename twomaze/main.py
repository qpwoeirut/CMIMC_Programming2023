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

args = parser.parse_args()

grader = TwoMazeGrader(args.pattern, args.debug)
grader.grade()
grader.print_result()