from maze_generators import generate_cycleless, generate_random
from carnegie import carnegie_1, carnegie_2, carnegie_3
from mellon import mellon_1, mellon_2, mellon_3
from pathlib import Path


class TwoMazeGrader:
    """
    TwoMaze grading class used to locally test a twomaze submission.
    """
    MAZES_DIR = Path(__file__).parent / "mazes"

    MAZE_SIZE = 32
    VIEW_SIZE = 8
    PROBLOW = 0.2
    PROBHIGH = 0.3
    MAXTURNS = 4096

    def __init__(self, maze_pattern=1, debug=False) -> None:
        """
        Initializes the grader with the maze pattern and debug flag.
        """

        # generate maze
        assert 1 <= maze_pattern <= 3, "Invalid maze pattern, must be 1, 2, or 3."
        self.maze_pattern = maze_pattern
        if self.maze_pattern == 1:
            self.walls_horizontal, self.walls_vertical = generate_random(
                self.PROBLOW, self.MAZE_SIZE)
        elif self.maze_pattern == 2:
            self.walls_horizontal, self.walls_vertical = generate_random(
                self.PROBHIGH, self.MAZE_SIZE)
        else:
            self.walls_horizontal, self.walls_vertical = generate_cycleless(
                self.MAZE_SIZE)

        # set carnegie and mellon functions
        self.carnegie_fn = [carnegie_1, carnegie_2,
                            carnegie_3][maze_pattern - 1]
        self.mellon_fn = [mellon_1, mellon_2, mellon_3][maze_pattern - 1]

        self.debug = debug

        # Print Maze
        if debug:
            row = [' '] * (2 * self.MAZE_SIZE + 1)
            for k in range(0, self.MAZE_SIZE):
                row[2*k+1] = '_'
            print(''.join(row))
            for j in range(self.MAZE_SIZE-1, -1, -1):
                for i in range(0, self.MAZE_SIZE):
                    row[2*i] = '|' if (self.walls_vertical[i][j] == 1) else ' '
                    row[2*i+1] = '_' if (self.walls_horizontal[i]
                                         [j] == 1) else ' '
                row[2*self.MAZE_SIZE] = '|'
                print(''.join(row))

    def _validated_output(self, output: tuple):
        """
        Basic output validation.
        """
        if type(output) != tuple:
            raise Exception("Invalid output format")
        if len(output) != 2:
            raise Exception("Invalid output format")
        if type(output[0]) != int or type(output[1]) != int:
            raise Exception("Invalid output format")
        return output

    def _localwall(self, robot_x, robot_y, walls_hv, robot_phase):
        walls_restricted = []
        for i in range(0, 2*self.VIEW_SIZE):
            walls_restricted.append([0] * (2*self.VIEW_SIZE))

        for i in range(0, 2*self.VIEW_SIZE):
            for j in range(0, 2*self.VIEW_SIZE):
                di = i - self.VIEW_SIZE
                dj = j - self.VIEW_SIZE
                if (robot_y + dj == self.MAZE_SIZE and (robot_phase)):
                    walls_restricted[i][j] = 1
                elif (robot_x + di == self.MAZE_SIZE and not (robot_phase)):
                    walls_restricted[i][j] = 1
                elif (robot_y + dj >= 0 and robot_y + dj < self.MAZE_SIZE and robot_x + di >= 0 and robot_x + di < self.MAZE_SIZE):
                    walls_restricted[i][j] = walls_hv[robot_x +
                                                      di][robot_y + dj]
                else:
                    walls_restricted[i][j] = 0

        return walls_restricted

    def _illegalmove(self, robot_x, robot_y, walls_horizontal, walls_vertical, robot_phase, move):
        if (move == 0):
            return False

        sign = bool(move > 0) - bool(move < 0)
        shift = bool(move < 0)

        if (robot_phase):
            # Vertical move
            if (robot_y + move < 0) or (robot_y + move >= self.MAZE_SIZE):
                return True
            for i in range(sign, move+sign, sign):
                if (walls_horizontal[robot_x][robot_y+i+shift] == 1):
                    return True

        else:
            # Horizontal move
            if (robot_x + move < 0) or (robot_x + move >= self.MAZE_SIZE):
                return True
            for i in range(sign, move+sign, sign):
                if (walls_vertical[robot_x+i+shift][robot_y] == 1):
                    return True

        return False

    def _grade_maze(self):
        """
        Grade the maze.
        """
        walls_horizontal = self.walls_horizontal
        walls_vertical = self.walls_vertical

        robot_clock_incs = [0]
        robot_x = 0
        robot_y = 0
        robot_phase = True
        robot_turns = 0

        while (robot_x != (self.MAZE_SIZE-1) or robot_y != (self.MAZE_SIZE-1)):
            # Obtain move
            if robot_phase:
                walls_restricted = self._localwall(
                    robot_x, robot_y, walls_horizontal, robot_phase)
                result = self._validated_output(self.carnegie_fn(
                    robot_x, robot_y, walls_restricted, robot_clock_incs))
            else:
                walls_restricted = self._localwall(
                    robot_x, robot_y, walls_vertical, robot_phase)
                result = self._validated_output(self.mellon_fn(
                    robot_x, robot_y, walls_restricted, robot_clock_incs))

            # Print debugging information
            if self.debug:
                rob = f"Carnegie" if robot_phase else f"Mellon  "
                print(
                    f"{rob} | Turn: {robot_turns} | Pos: {robot_x},{robot_y} | Move: {result[0]} | Increment: {result[1]}")

            # Validate move
            if (self._illegalmove(robot_x, robot_y, walls_horizontal, walls_vertical, robot_phase, result[0])):
                raise Exception("Illegal move.")

            # Update move
            if robot_phase:
                robot_y += result[0]
            else:
                robot_x += result[0]

            # Validate clock
            clock_inc = result[1]
            if (clock_inc <= 4):
                raise Exception("Illegal clock incrementation.")

            # Validate turns
            robot_turns += 1
            if (robot_turns > self.MAXTURNS):
                raise Exception(
                    "Exceeded maximum number (4096) of Carnegie/Mellon calls.")

            # Update clock
            robot_phase = not robot_phase
            robot_clock_incs.append(clock_inc)

        total_time = sum(robot_clock_incs)
        return total_time

    def grade(self) -> None:
        """
        Grades the maze.
        """
        try:
            self.result = self._grade_maze()
        except Exception as e:
            self.result = repr(e)

    def print_result(self) -> None:
        """
        Prints the result of the grading.
        """
        print("Result: " + str(self.result))
