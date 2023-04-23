"""
Usage:
    python3 visualizer.py
    python3 visualizer.py FILENAME

NOTE: You must run a game first and save it's results (see main.py) to generate 
the history file ("history.game"), which is then read and visualized by this file. 
You can also visualize an online game by downloading the save file, 
put it in the same folder as the visualizer, and run 
`python3 visualizer.py FILENAME`


This visualizer depends on a pip package, which can be installed by running:
`pip install -r requirements.txt`

In the visualizer, use the arrow keys to navigate through the turns and players.
Up/Down will change the player, and Left/Right will change the turn. The current
player and turn are printed in the terminal.

The visualizer shows the board at each turn, from the perspective of one player 
at a time.

Each cell contains a number- the total number of settlements in that cell across 
all players.

Every '#' in a cell indicates that one of the settlements was placed by the 
current player at some point in time. For example, if the cell says 3##, then 
there are 3 settlements total in the cell, 2 of which were placed by the current 

Every '+' indicates that one of the settlements in that cell was placed by the 
current player in the current turn. For example, if the cell says 3##+, then 
there are 3 settlements total, 2 of which were placed by the current player, 
and 1 of which was placed by the current player in the current turn.

'B' indicates that that cell was bombed at the end of the turn.

Note that the number in the cell, #'s, and +'s are all the numbers before the 
bombs are released.

The message bar below gives the current round, selected player, and scores for each player.
For a downloaded game, your program is assigned with a random player id between 0 - 4.
The visualizer will show which player is controlled by your code. For a local game, the default player
is set to 0. (ignore it in local games)

Recall that if your program exceeds the query time, total time, or memory limit, or gives an invalid
output, your settlements will be placed down randomly. Whenever that happens, the visualizer will display
a text message to indicate that your program did not operate normally in a given turn.
"""

from grid import Grid
import game2dboard
import copy
from pathlib import Path
import sys

exceptions = {1:"You program fail to produce a valid move!\nYour move in the current turn is random.", 0:""}

if len(sys.argv) > 1:
    inFile = sys.argv[1]
    print(inFile)
else:
    inFile = "history.game"



# Read from save
import pickle
try:
    pid, record_compressed, error = pickle.load(open(Path(__file__).parent / inFile, "rb" ))
    turns = len(record_compressed)
except:
    pid, record_compressed = pickle.load(open(Path(__file__).parent / inFile, "rb" ))
    turns = len(record_compressed)
    error = [0 for _ in range(turns)]

# Run the game
grid = Grid()
SIZE, SETTLEMENTS, PLAYERS, BOMBS = 10, 3, 5, 2


scores = []
boards = []
totals = []
bombs = []
avgs = []
avg = [0]*5
for step in range(turns):
    recorded_moves, recorded_bombs = record_compressed[step]
    grid.simulate_step(recorded_moves)

    scores.append(copy.deepcopy(grid.score()))
    boards.append(copy.deepcopy(grid.grid))
    totals.append(copy.deepcopy(grid.grid_sum))
    
    bombs.append(recorded_bombs)

    for i in range(PLAYERS):
        avg[i] = (avg[i]*step + scores[step][i])/(step + 1)
    avgs.append(copy.deepcopy(avg))

    grid.simulate_bombs(recorded_bombs)

# Move
def on_key_press(keysym):
    global turn
    global player
    if keysym == 'Right':
        turn = min(turns - 1, turn + 1)
    if keysym == 'Left':
        turn = max(0, turn - 1)
    if keysym == 'Down':
        player = min(PLAYERS - 1, player + 1)
    if keysym == 'Up':
        player = max(0, player - 1)
    board = boards[turn]
    total = totals[turn]
    score = scores[turn]
    avg = avgs[turn]

    for i in range(SIZE):
        for j in range(SIZE):
            total[i][j] = str(total[i][j])
    bd.load(total)

    # settlements that were made by the current player in total
    for i in range(SIZE):
        for j in range(SIZE):
            for _ in range(board[i][j][player]):
                bd[i][j] = f"{bd[i][j]}#"

    # settlements that were made by the current player in this turn
    for pos in record_compressed[turn][0][player]: 
        bd[pos[0]][pos[1]] = f"{bd[pos[0]][pos[1]]}+"              
    
    for b in bombs[turn]:
        for pos in grid._bomb_coords(b[0], b[1]):
            bd[pos[0]][pos[1]] += "B"
    scorestrcolor = f"Round {turn+1}\nShowing player {player}" + ("(your program)" if player == pid else "") + "\n" + exceptions[error[turn]] +  "\n" + "".join([("\033[91m" if i == pid else "") + f"                Player {i}: {score[i]}; Avg: {round(avg[i],1)}"+("<" if i == player else "") +("\033[0m" if i == pid else "") + "\n" for i in range(PLAYERS)])

    scorestr = f"Round {turn+1}\nShowing player {player}" + ("(your program)" if player == pid else "") + "\n" + exceptions[error[turn]] + "\n" +  "".join([("\u0332" if i == pid else "").join(f"               Player {i}: {score[i]}; Avg: {round(avg[i],1)}"+("<" if i == player else "") + "\n") for i in range(PLAYERS)])
    print(scorestrcolor)
    bd.print(scorestr)
    
try:
    import matplotlib.pyplot as plt
    fig = plt.Figure()
    ax = fig.add_subplot()
    for i in range(5):
        ax.plot(list(range(turns)), [scores[_][i] for _ in range(turns)], label = f'Player {i}' + ('(you)' if i == pid else ''))
    fig.legend()
    fig.savefig("fig.png") 
except ImportError as e:
    print("Install `matplotlib` to plot scores!")
    print(e)

bd = game2dboard.Board(SIZE, SIZE)
bd.title = "Lebomb Visualizer"
bd.grid_color = "DarkSlateBlue"
bd.cell_color = "LightCyan"
bd.cell_size = 45
    
# Visualize
turn = 0
player = pid
print(f"You are player {pid}")
bd.create_output(font_size = 14)
bd.on_key_press = on_key_press

on_key_press('')
bd.show()
try: # i will never understand how to plot in python...
    from PIL import Image

    image = Image.open('fig.png')
    image.show()
except:
    print("Open `fig.png` in the folder")
    pass