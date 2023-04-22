from grid import Grid
from strategy import get_strategies
import copy
import random

class LebombJamesGrader:

    TURNS = 1000

    def __init__(self, debug=False, save=False) -> None:
        self.debug = debug
        self.save = save

    def _validated_move(self, move):
        # return random move if move is invalid
        try:
            assert type(move) == list, "Must return a list"
            assert len(move) == 3, "Must have 3 moves"
            for m in move:
                assert type(m) == tuple, "Must return a list of tuples"
                assert len(m) == 2, "Must return a list of tuples of length 2"
                assert type(m[0]) == int, "Must return a list of tuples of ints"
                assert type(m[1]) == int, "Must return a list of tuples of ints"
                assert 0 <= m[0] <= 9, "Must return a list of tuples of ints between 0 and 9"
                assert 0 <= m[1] <= 9, "Must return a list of tuples of ints between 0 and 9"
            return move
        except AssertionError as ex:
            if self.debug:
                print(ex)

            return [
                (random.randint(0, 9), random.randint(0, 9)), 
                (random.randint(0, 9), random.randint(0, 9)), 
                (random.randint(0, 9), random.randint(0, 9)), 
            ]
    
    def _grade_grid(self) -> int:
        """
        Grades the grid and returns the final score.
        """
        grid = Grid()
        strategies = get_strategies()
        assert len(strategies) == 5, "Must have 5 strategies"

        for _ in range(self.TURNS):
            # retrieve moves
            moves = []
            for i, strategy in enumerate(strategies):
                move = self._validated_move(strategy(i, copy.deepcopy(grid.state())))
                moves.append(move)
            
            grid.step(moves)

        # calculate score
        total_scores = [0] * 5
        for round_score in grid.scores:
            for i, score in enumerate(round_score):
                total_scores[i] += score
        for i in range(5):
            total_scores[i] = total_scores[i] / len(grid.scores)

        if self.save:
            grid.dump()
            
        return total_scores

    def grade(self) -> int:
        """
        Grades the submission and sets the result variable.
        """
        self.result = self._grade_grid()

    def print_result(self) -> None:
        """
        Prints the results of the grading.
        """
        print("Results:")
        if type(self.result) == str: # error occurred
            print(self.result)
        else:
            for i, score in enumerate(self.result):
                print(f"Player {i}: {score}")