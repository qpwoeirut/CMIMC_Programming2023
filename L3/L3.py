"""
L3, designed for the 2023 CMIMC Programming Contest New Language Round
Designed by Kevin You
Use the -x flag to run code in L3X.
Use the -c flag to select code (csv file)
Use the -t flag to specify your task number
Use the -d flag to get debugging information

For example, this command runs your code in code.csv on task 1:

python3 L3.py -c code.csv -t 1
"""

import sys
import string
import getopt
import operator
import queue
import copy
import json
from pathlib import Path

PRIMES = [2,3,5,7,11,13,17,19,23,29]
MAXNUM = 30
MAXTIME = 10000
MAXGRID = 100
MAXM = 10

class data:
    def __init__(self, value, x, y, direc):
        self.value, self.x, self.y, self.direc = value, x, y, direc

    def movein(self, direction):
        self.x += direction[0];
        self.y += direction[1];
        self.direc = direction

    def moveop(self, direction):
        self.x -= direction[0];
        self.y -= direction[1];
        self.direc = (-direction[0],-direction[1])

    def str(self):
        return "Number [" + ",".join(str(x) for x in self.value) + "] on square (" + str(self.x) + "," + str(self.y)  \
                + "), traveling in direction " + str(self.direc)

def primefactor(a):
    assert(a <= MAXNUM)
    out = []
    for p in PRIMES:
        vp = 0
        while a % pow(p, vp+1) == 0:
            vp += 1
        out.append(vp)
    return out

def main():
    debug = False
    extended = False
    code = ""
    trace = ""

    try:
        opts, args = getopt.getopt(sys.argv[1:], "dxc:t:", ["debug", "extended", "code = ", "test = "])
    except getopt.GetoptError as err:
        print(err, file=sys.stderr)
        sys.exit(1)

    for o, a in opts:
        if o in ("-d", "--debug"):
            debug = True
        if o in ("-x", "--extended"):
            extended = True
        elif o in ("-c", "--code"):
            code = a
        elif o in ("-t", "--task-number"):
            trace = Path(__file__).parent / "publictestcases" / f"publictest{a}.json"

    if len(sys.argv) == 1 or code == "" or trace == "":
        print("Hello! To execute L3 code, run the interpreter with argument to -c specifying the code file \
               and argument to -t specifying the test file")

    with open(code) as file:
        lines = [line.rstrip() for line in file]

    height = len(lines)
    if height == 0:
        print("Parse Error: Empty file", file=sys.stderr)
        sys.exit(1)
    width = len(lines[0].split(','))

    if height > MAXGRID or width > MAXGRID:
        print("Parse Error: Dimensions of grid exceed " + str(MAXGRID), file=sys.stderr)
        sys.exit(1)

    if extended and width < 2:
        print("Parse Error: Width in L3X must be at least 2", file=sys.stderr)
        sys.exit(1)

    codes, directions, watchpoints, queues = [], [], [], []
    for i in range(0, height):
        codes.append([])
        directions.append([])
        watchpoints.append([])
        queues.append([])
        for j in range(0, width):
            codes[i].append(0)
            directions[i].append((0,0))
            watchpoints[i].append(False)
            queues[i].append(0)

    for i in range(0, height):
        instructions = lines[i].split(',')
        if len(instructions) != width:
            print("Parse Error: Inconsistent row length", file=sys.stderr)
            sys.exit(1)

        for j in range(0, width):
            loc = "Parse Error at (" + str(i) + "," + str(j) + "):"

            k = instructions[j]
            if len(k) == 0:
                continue

            if (k[-1] == ';'):
                watchpoints[i][j] = True
                k = k[:-1]

            head = k.rstrip(string.ascii_letters)
            tail = k[len(head):]

            if head in ['%','&','~']:
                if not extended: 
                    print(loc + " Not in L3X. Please try again with the -x flag", file=sys.stderr)
                    sys.exit(1)
                else:
                    codes[i][j] = head

            else: 
                if int(head) > MAXNUM or int(head) < 0:
                    print(loc + " Invalid number/operation.", file=sys.stderr)
                    sys.exit(1)
                else:
                    codes[i][j] = primefactor(int(head))

            if tail not in ['n','s','w','e','N','S','W','E','u','d','l','r','U','D','L','R']: 
                print(loc + " Invalid direction.", file=sys.stderr)
                sys.exit(1)
            else:
                if tail == 'n' or tail == 'N' or tail == 'u' or tail == 'U':
                    directions[i][j] = (-1,0)
                if tail == 's' or tail == 'S' or tail == 'd' or tail == 'D':
                    directions[i][j] = (1,0)
                if tail == 'w' or tail == 'W' or tail == 'l' or tail == 'L':
                    directions[i][j] = (0,-1)
                if tail == 'e' or tail == 'E' or tail == 'r' or tail == 'R':
                    directions[i][j] = (0,1)

    if extended and codes[0][1] != '&':
        print("Parse Error: Missing required & square at (0,1) in L3X", file=sys.stderr)
        sys.exit(1)

    f = open(trace)
    tests = json.load(f)
    f.close()

    numcase = 0
    passcase = 0

    for case in tests:

        for i in range(0, height):
            for j in range(0, width):
                if codes[i][j] == "&":
                    queues[i][j] = queue.Queue()

        Mumbers = []
        Mumbers.append(data(case['input'],0,0,(1,0)))

        if extended:
            for i in case['instream']:
                queues[0][1].put(i)

        if debug:
            print("Input is " + str(case['input']))
            if extended:
                print("Input stream is " + str(case['instream']))

        output = False
        runerror = False
        outnum = []
        outqueue = queue.Queue()
        counter = 0

        loc = "Runtime Error on test case " + str(numcase) + ":"

        while (not output and not runerror and counter < MAXTIME):

            counter += 1

            new = []
            disappear = []

            for M in Mumbers:

                if M.x == height and M.y == width-1:
                    output = True
                    outnum = M.value
                    break

                elif extended and M.x == height and M.y == width-2:
                    outqueue.put(M.value)
                    disappear.append(M)
                    continue

                elif M.x >= height or M.x < 0 or M.y >= width or M.y < 0:
                    print(loc + " Number out of bounds.", file=sys.stderr)
                    runerror = True
                    break

                currn = codes[M.x][M.y]
                currdir = directions[M.x][M.y]

                if type(currn) == int and currn == 0:
                    print(loc + " Number on blank square at (" + str(M.x) + "," + str(M.y) + ")", file=sys.stderr)
                    runerror = True
                    break

                if debug and watchpoints[M.x][M.y]:
                    print(M.str())

                if type(currn) == str:
                    if currn == "~":
                        M.value = [0] * len(PRIMES)
                        M.movein(currdir)

                    elif currn == "%":
                        W = copy.deepcopy(M)
                        new.append(W)

                        M.movein(currdir)
                        W.moveop(currdir)

                    elif currn == "&":
                        if currdir == M.direc:
                            queues[M.x][M.y].put(M.value)
                            disappear.append(M)

                        else:
                            if queues[M.x][M.y].empty():
                                print(loc + " Empty queue at (" + str(M.x) + "," + str(M.y) + ")", file=sys.stderr)
                                runerror = True
                                break
                            else:
                                W = queues[M.x][M.y].get()
                                M.value = [x+y for (x,y) in zip(M.value, W)]
                                M.movein(currdir)

                elif type(currn) == list:
                    if currdir == M.direc:
                        M.value = [x+y for (x,y) in zip(M.value, currn)]
                        M.movein(currdir)

                    else:
                        if all([x >= y for (x,y) in zip(M.value, currn)]):
                            M.value = [x-y for (x,y) in zip(M.value, currn)]
                            M.movein(currdir)
                        else: 
                            M.moveop(currdir)

            if output or runerror:
                break

            Mumbers = Mumbers + new
            if len(disappear) > 0:
                Mumbers = [x for x in Mumbers if x not in disappear]

            if (len(Mumbers) > MAXM):
                print(" Over " + str(MAXM) + " active numbers.", file=sys.stderr)
                runerror = True
                break

            locs = []
            for M in Mumbers:
                if (M.x, M.y) in locs:
                    print("Two numbers collided on square (" + str(M.x) + "," + str(M.y) + ")", file=sys.stderr)
                    runerror = True
                    break
                else:
                    locs.append((M.x, M.y))

        if (output):
            if outnum == case['output']:
                if extended:
                    outlist = []
                    while (not outqueue.empty()):
                        outlist.append(outqueue.get())

                    if outlist == case['outstream']:
                        passcase += 1
                        if debug:
                            print("Passed case " + str(numcase))
                    else:
                        if debug:
                            print("Failed case " + str(numcase))
                            print("Intended output stream is " + str(case['outstream']) + \
                                  ", actual output stream is " + str(outlist))
                else:
                    passcase += 1
                    if debug:
                        print("Passed case " + str(numcase))
            else:
                if debug:
                    print("Failed case " + str(numcase))
                    print("Intended output is " + str(case['output']) + ", actual output is " + str(outnum))

        elif (runerror):
            if debug:
                print("Failed case " + str(numcase))

        else:
            assert(counter == MAXTIME)
            print("Runtime Error: Exceeded " + str(MAXTIME) + " steps.", file=sys.stderr)
            if debug:
                print("Failed case " + str(numcase))

        numcase = numcase + 1

    # This is the only information that contestants should recieve if their submission is for grading
    # They should not be able to read prints under debug or prints to stderr (these are for local testing only)

    score = width * height
    print("Passed " + str(passcase) + "/" + str(numcase) + " test cases.")
    print("The area of your code is " + str(score) + " squares.")


if __name__ == '__main__':
    main()

 
