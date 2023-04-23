"""
Edit this file! This is the file you will submit.
"""
import random

# Implement me!
# 2 example strategies to use in your tournament.



a = []
c = 0
cur = 0


def wins(wallet, history):
    sm = 100
    l = 0
    for i, j in history:
        sm -= i
        if j == False:
            l += 1
    return sm, l


def getmed():
    a.sort()
    n = len(a)
    if (n == 0):
        return 10
    return a[n // 2]


# conservatively destroy other teams (if 3 losses + less than threshold)
def consdest(wallet, history):
    th = 12
    z = wins(wallet, history)
    if (z[0] < th) and (z[1] >= 3):
        return z[0] + 1

    return min(wallet, 3)


# always play conservative (at most 3)
def cons(wallet, history):
    return min(wallet, 3)


# attack other teams (if less than threshold)
def consatk(wallet, history):
    th = 12
    z = wins(wallet, history)
    if z[0] < th:
        return z[0] + 1
    return min(wallet, 3)


# attack whenever possible
def atk(wallet, history):
    z = wins(wallet, history)
    return min(wallet, z[0] + 1)


# random under threshold
def consrand(wallet, history):
    th = 12
    return min(wallet, random.randint(0, th))


# random under threshold but above 5
def consrand2(wallet, history):
    th = 12
    return min(wallet, random.randint(th / 2, th))


# powers of 2
def powers(wallet, history):
    z = len(history)
    return min(wallet, pow(2, z))


# bet 1/5 each time
def fifth(wallet, history):
    return wallet / 5


# bet 1/7 each time
def seventh(wallet, history):
    return wallet / 7


# bet 1/8 each time
def eighth(wallet, history):
    return wallet / 8


# bet 1/6 each time
def sixth(wallet, history):
    return wallet / 6


# bet 1/9 each time
def ninth(wallet, history):
    return wallet / 9


def tenth(wallet, history):
    return wallet / 10


# powers of 2 but no more than 15
def conspow(wallet, history):
    z = len(history)
    return min(wallet, 20, pow(2, z))

# always guess 7
def seven(wallet, history):
    return min(wallet, 7)


def six(wallet, history):
    return min(wallet, 6)


def eight(wallet, history):
    return min(wallet, 8)


# randomish strategy
def smart(wallet, history):
    z = wins(wallet, history)

    if (z[0] <= 10):
        return z[0] + 1

    if (z[1] == 4):
        if (z[0] <= 15):
            return z[0] + 1
        return 0

    if (z[1] == 3):
        return min(wallet, 7)

    return min(wallet, 3)


# bet seven + hope some other things work
def smarterseven(wallet, history):
    z = wins(wallet, history)
    th = 12
    if (z[1] == 4 and z[0] > 7):
        return min(wallet, random.randint(0, th))

    return min(wallet, z[0] + 1, 7)


# bet seven + hope some other things work
def smartseven(wallet, history):
    z = wins(wallet, history)

    return min(wallet, z[0] + 1, 7)


def five(wallet, history):
    z = wins(wallet, history)

    return min(wallet, 5)


def risky(wallet, history):
    return min(wallet, random.randint(10, 15))


# troll
def troll(wallet, history):
    th = 12
    z = wins(wallet, history)
    sz = len(history)
    if (sz >= 3):
        return min(wallet, th)

    return min(wallet, 1)


def half(wallet, history):
    return wallet // 2


def fifteen(wallet, history):
    return min(wallet, 15)

def largeatfirst (wallet, history):
    if (wallet == 100):
        return 12
    if (wallet == 88):
        return 2
    if (wallet == 86):
        return 10
    if (wallet == 76):
        return 2
    if (wallet == 60):
        return 2
    return min(wallet, 7)

cturns = 0
def zeroinitial (wallet, history):
    global cturns
    cturns += 1
    if (cturns == 1):
        return 0
    if (cturns == 2):
        return 0
    if (cturns == 3):
        return 0
    if (cturns == 4):
        return 30
    if (cturns == 5):
        return 30
    return min(wallet, 8)

turns = 0
def betterthanreveng(wallet, history):
    z = wins(wallet, history)
    th = 10
    guess = []
    cnt = 0
    cnt2 = 0
    mx = 0
    global turns
    turns += 1
    for i, j in history:
        guess.append(i)
        if i > th:
            cnt += 1
        if i > 2 * th:
            cnt2 += 1
        if i > mx:
            mx = i

    sz = len(history)

    if turns == 1:
        return 1

    if turns == 2:
        return 13

    if turns == 3:
        return 12

    if turns == 4:
        return 13

    res = 100

    guess.sort()
    if sz > 0:
        res = guess[sz//2]

    res = min(res, z[0])

    #if we've played 8 turns, the player we are playing against is considered to be a conservative player
    #  if (sz >= 5 and res >= 2 * th and 5 * cnt2 >= 4 * sz):
    #     return 0

    # if (sz >= 10 and res >= th and 5 * cnt >= 4 * sz):
    #     return 0



    if (wallet >= res + 1 and res + 1 <= th):
        return res + 1

    if (turns <= 6 and cnt2 * 2 >= turns):
        par = random.randint(0,1)
        if (par % 2):
            return min(wallet, res + 1)
        return 0

    if (wallet >= th and z[0] <= 2 * th):
          return th

    return min(wallet, res + 1, th//2)



# take opponents maximum frequency guess + 1 if below the threshold, otherwise take 7
def reveng(wallet, history):
    th = 12
    z = wins(wallet, history)
    #  for i,j in history:
    #     if j == True:
    #        a.append(i)
    # th = 2 * getmed()
    res = 100
    guess = []
    cnt = 0
    cnt2 = 0
    mx = 0
    for i, j in history:
        guess.append(i)
        if i >= th:
            cnt += 1
        if i >= 2 * th:
            cnt2 += 1
        if i > mx:
            mx = i
    sz = len(guess)

    if (sz == 0):
        return min(wallet, random.randint(10, 15))

    if (sz > 0):
        res = max(set(guess), key=guess.count)

    if (sz >= 2 and sz <= 4 and cnt2 == sz and z[0] >= wallet):
        return 0

    if (sz >= 7 and 5 * cnt >= sz * 4):
        return min(wallet, z[0] + 1, th)

    res = min(res, z[0])
    if (wallet >= res + 1 and res + 1 <= th):
        return res + 1
    return min(wallet, res + 1, 7)


# troll bot from LIT server
def vivek_troll00(wallet, history):
    if len(history) <= 0:
        return min(random.randint(6, 7), wallet)
    if history[0][0] < 4:
        return min(history[0][0] + 1, wallet)
    return min(random.randint(6, 7), wallet)


# plot to destroy best bot
def killreveng(wallet, history):
    th = 12
    z = wins(wallet, history)
    sz = len(history)

    res = z[0]
    if (sz <= 2):
        return min(wallet, 2 * th + 1)

    return min(wallet, res + 1, 7)


# hope for some score, then try to achieve that score

val = 10


def pluw(wallet, history):
    z = wins(wallet, history)
    sz = len(history)
    global val
    if (sz % 3 == 0):
        val = min(wallet, (wallet + 9) // 10)
    return val


# actually dumber version of reveng
gtturns = 0
def revengsmart(wallet, history):
    z = wins(wallet, history)
    global gtturns
    gtturns += 1
    if (gtturns == 0):
        return 0
    th = 12
    res = 100
    guess = []
    for i, j in history:
        guess.append(i)
    sz = len(guess)
    if (sz > 0):
        res = max(set(guess), key=guess.count)
    res = min(res, z[0])
    if guess.count(res) >= sz / 3 and wallet >= res + 1 and res + 1 <= th:
        return res + 1

    if wallet >= res + 1 and res + 1 <= th:
        par = random.randint(0,1)
        if (par % 2):
            return res + 1

    return min(wallet, res + 1, 7)

ind = 0
b = [16,16,16,9,8,8,6,6,4,4,2,2,2,1]
random.shuffle(b)
def randperm(wallet, history):
    global ind
    ind += 1

    if (ind > len(b)):
        return 0

    return b[ind-1]

lb = 0
copyturns = 0
def copycat(wallet, history):
    th = 8
    global lb
    global copyturns
    copyturns += 1
    z = wins(wallet, history)
    sz = len(history)
    if (copyturns == 0):
        return 1
    if (copyturns == 1):
        return 0
    elif sz == 0:
        return 1
    ans = min(wallet, z[0] + 1, history[sz-1][0] + 1)
    ans = min(ans, 2 * th)
    return ans

# attempt to troll good strategies by providing horrible data
def scare(wallet, history):
    th = 12
    z = wins(wallet, history)
    if (len(history) <= 3):
        return min(wallet, th)
    res = z[0]

    return min(wallet, res + 1, 8)



def gambler(wallet, history):
    return random.randint(0, wallet)

def gambleragain(wallet, history):
    return min(wallet, random.randint(10, 30))


def low(wallet, history):
    z = wins(wallet, history)

    if (z[0] < wallet and z[1] == 4):
        return z[0] + 1
    return random.randint(0, 3)


def villain(wallet, history):
    return max(wallet - 1, 0)

def mixed (wallet, history):
    par = random.randint(0,30)
    if par == 4:
        return zeroinitial(wallet, history)
    if par == 7:
        return copycat(wallet, history)
    return betterthanreveng(wallet,history)


curturns = 0
curloss = 0
def best(wallet, history):
    z = wins(wallet, history)
    th = 10
    res = 100
    guess = []
    cnt = 0
    cnt2 = 0
    mx = 0
    for i, j in history:
        guess.append(i)
        if i > th:
            cnt += 1
        if i > 2 * th:
            cnt2 += 1
        if i > mx:
            mx = i
    sz = len(guess)

    global curturns
    global curloss
    curturns += 1

    if (curturns >= 9):
        th = th//2
    if (curturns == 1):
        curloss += 6 #6/10 chance that we lose with 2
        return 1
    if (curturns <= 4):

        if (cnt >= 2):
            if (z[0] + 1 > th//2):
                curloss += 4
            return min(wallet, z[0] + 1, th//2)

        tmpval = 14

        if (tmpval >= z[0] + 1):
            tmpval = z[0] + 1
        else:
            curloss += 2
        return min(wallet, z[0] + 1, tmpval)

    if (wallet > 2 and curloss//10 > 4): #assume we only have like 3 turns left max
        if (z[1] == 4):
            return min(wallet, z[0] + 1, max(1,wallet-1))
        return min(wallet, z[0] + 1, max(1, wallet - 3))

    if (z[1] == 4):
        if (wallet >= z[0] + 1 and z[0] + 1 <= th):
            return z[0] + 1
        if (curloss//10 == 3):
            if (wallet >= z[0] + 1 and z[0] + 1 <= 2 * th):
                return z[0] + 1
            else:
                return min(wallet, 1)

    if (curloss//10 > z[1]):
        if (wallet >= z[0] + 1 and z[0] + 1 <= 2 * th):
            return z[0] + 1
        if (cnt >= 2):
            curloss += 2
            return min(wallet, th + 2)
        curloss += 1
        return min(wallet, 2 * th)

    if (curloss//10 < z[1]):
        if (wallet >= z[0] + 1 and z[0] + 1 <= th):
            return z[0] + 1
        curloss += 8
        return min(wallet, 3)

    curloss += 4
    return min(wallet, th)


#copy from the best team form the last game

clowncounter = 0
def clown(wallet, history):
    global clowncounter
    clowncounter += 1
    a = [3,11,7,2,12,10,6,3,1,2,5,6,1,2,2,2,2,1,1]

    if (clowncounter - 1 >= len(a)):
        return min(wallet, 1)
    return a[clowncounter - 1]
# Edit me!
def get_strategies():
    """
    Returns a list of strategy functions to use in a tournament.

    In the local tester, all of the strategies will be used as separate bidders in the tournament.
    Note that strategies are tracked by their function name for readability in the results, so
    adding the same function multiple times will not simulate multiple bidders using the same strategy.

    In the official grader, only the first element of the list will be used as your strategy.
    """
    strategies = [
                     copycat, betterthanreveng,
                     #mixed
                  zeroinitial, randperm,
                  vivek_troll00, smartseven, gambler, villain, consrand, atk, consatk, cons, consdest,
                consrand2, seven, powers, fifth, conspow, tenth, six, eight, seventh, eighth, ninth, smart,
                  five, smarterseven, revengsmart, scare, killreveng, troll, half, low, pluw, risky,
                 fifteen, reveng, zeroinitial,gambleragain,
                 clown,
                    # largeatfirst,
                best] +\
                ([largeatfirst]) \
                 + ([zeroinitial]) * 5 +([clown]) * 10
                 # + ([copycat]) * 10

    return strategies
