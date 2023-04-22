import random
import copy
import pickle
from pathlib import Path
from json import dumps

class Grid:
    """
    Grid class used to simulate the game
    """
    SIZE = 10
    SETTLEMENTS = 3
    PLAYERS = 5
    BOMBS = 2

    MAX_TURNS = 1000
    SCORED_TURNS = 100

    def __init__(self) -> None:
        self.grid = [[[0] * self.PLAYERS for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        self.grid_sum = [[0] * self.SIZE for _ in range(self.SIZE)]
        self.history = []
        self.scores = []
        self.turn = 1

    def step(self, moves):
        """
        Play the game for one step

        moves: list of length 3 lists of (x,y) tuples
        """
        if self.turn > self.MAX_TURNS:
            raise Exception("Game has ended")

        # place settlements
        for player in range(self.PLAYERS):
            for x, y in moves[player]:
                self.grid[x][y][player] += 1
                self.grid_sum[x][y] += 1

        # place bombs
        placed_bombs = []

        while len(placed_bombs) < self.BOMBS:
            x, y = self._best_bomb()
            self._bomb(x, y)
            placed_bombs.append((x, y))

        # add scores
        if self.turn > self.MAX_TURNS - self.SCORED_TURNS:
            self.scores.append(self.score())

        self.turn += 1
        self.history.append((copy.deepcopy(moves), placed_bombs))
    
    def simulate_step(self, moves):
        """
        Simulate the game for one step, to use in the visualizer when loading a game history

        moves: list of length 3 lists of (x,y) tuples
        bombs: list of (x,y) tuples
        """
        if self.turn > self.MAX_TURNS:
            raise Exception("Game has ended")

        # place settlements
        for player in range(self.PLAYERS):
            for x, y in moves[player]:
                self.grid[x][y][player] += 1
                self.grid_sum[x][y] += 1

        self.turn += 1
    
    def simulate_bombs(self, bombs):
        """
        bombs: list of (x,y) tuples
        """
        for x, y in bombs:
            self._bomb(x, y)

    def state(self):
        """
        Get the current state of the game
        """
        return self.grid
    
    def dump(self):
        """
        Dump the game history into the file history.game, using 0 as the default player
        """
        pickle.dump((0, self.history), open(Path(__file__).parent / "history.game", "wb"))

    def score(self):
        """
        Return the current score of the game
        """
        cur_scores = [0] * self.PLAYERS
        for i in range(self.SIZE):
            for j in range(self.SIZE):
                if self.grid_sum[i][j] == 0:
                    continue

                for pid in range(self.PLAYERS):
                    cur_scores[pid] += self.grid[i][j][pid]
        return cur_scores

    def _bomb(self, x, y):
        """
        Bomb the given coordinates
        """
        bomb_coords = self._bomb_coords(x, y)
        for x, y in bomb_coords:
            if self.grid_sum[x][y] == 0:
                continue

            self.grid_sum[x][y] = 0
            for player in range(self.PLAYERS):
                self.grid[x][y][player] = 0

    def _best_bomb(self):
        """
        Get the bomb that destroys the most settlements
        """
        bombs = {}

        for i in range(self.SIZE):
            for j in range(self.SIZE):
                if self.grid[i][j] == 0:
                    continue

                bomb_coords = self._bomb_coords(i, j)

                settlements_destroyed = 0
                for x, y in bomb_coords:
                    settlements_destroyed += self.grid_sum[x][y]
                bombs[(i, j)] = settlements_destroyed
        
        mx_settlements = max(bombs.values())
        best_bombs = [bomb for bomb, settlements in bombs.items() if settlements == mx_settlements]
        return random.choice(best_bombs)

    def _bomb_coords(self, x, y):
        """
        Return list of coordinates of the bomb shape
        """
        bomb_coords = [(x, y)]
        if x > 0:
            bomb_coords.append((x-1, y))
        if x < self.SIZE-1:
            bomb_coords.append((x+1, y))
        if y > 0:
            bomb_coords.append((x, y-1))
        if y < self.SIZE-1:
            bomb_coords.append((x, y+1))
        return bomb_coords
