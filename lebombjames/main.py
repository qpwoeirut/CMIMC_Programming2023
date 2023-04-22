"""
Lebomb James local runner command line interface.

Usage:
    python main.py [-d] [-s] [--help]
"""

import argparse
from grader import LebombJamesGrader

parser = argparse.ArgumentParser(description="LebombJames local runner CLI")

parser.add_argument("--debug", "-d", action="store_true")
parser.add_argument("--save", "-s", action="store_true")

args = parser.parse_args()

grader = LebombJamesGrader(args.debug, args.save)
grader.grade()
grader.print_result()
