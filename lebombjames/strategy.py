"""
Edit this file! This is the file you will submit.
"""
import random

# Implement me!
def strategy(pid, board):
    return [(0, 0), (0, 0), (0, 0)]

# A random strategy to use in your game.
def random_strategy(pid, board):
    return [
        (random.randint(0, 9), random.randint(0, 9)), 
        (random.randint(0, 9), random.randint(0, 9)), 
        (random.randint(0, 9), random.randint(0, 9)), 
        ]

# Edit me!
def get_strategies():
    """
    Returns a list of strategy functions to use in a game.

    In the local tester, all of the strategies will be used as separate players in the game.
    Results will be printed out in the order of the list.

    In the official grader, only the first element of the list will be used as your strategy. 
    """
    strategies = [strategy, random_strategy, random_strategy, random_strategy, random_strategy]

    return strategies
