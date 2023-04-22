"""
Auction House local runner command line interface.

Usage:
    python main.py [-d] [-n NUM_TOURNAMENTS] [--help]
"""

import argparse
from grader import AuctionHouseGrader

parser = argparse.ArgumentParser(description="AuctionHouse local runner CLI")

parser.add_argument("--debug", "-d", action="store_true")
parser.add_argument("--num_tournaments", "-n", type=int, default=10)

args = parser.parse_args()

grader = AuctionHouseGrader(args.num_tournaments, args.debug)
grader.grade()
grader.print_result()