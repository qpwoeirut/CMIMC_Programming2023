"""
Edit this file! This is the file you will submit.
"""
import random

# Implement me!
# 2 example strategies to use in your tournament.


th = 12
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
    z = wins(wallet, history)
    if (z[0] < th) and (z[1] >= 3):
        return z[0] + 1

    return min(wallet, 3)


# always play conservative (at most 3)
def cons(wallet, history):
    return min(wallet, 3)


# attack other teams (if less than threshold)
def consatk(wallet, history):
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
    return min(wallet, random.randint(0, th))


# random under threshold but above 5
def consrand2(wallet, history):
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

#takes risk in the first 4 turns
riskvar = 0
def calcrisk (wallet, history):
    z = wins(wallet, history)
    global riskvar
    if (riskvar > 10):
        return min(wallet,z[0] + 1, 2)
    return min(wallet,z[0] + 1, 9)

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


def risky (wallet, history):
    return min(wallet, random.randint(10, 15))

# troll
def troll(wallet, history):
    z = wins(wallet, history)
    sz = len(history)
    if (sz >= 3):
        return min(wallet, th)

    return min(wallet, 1)


def half(wallet, history):
    return wallet // 2

turns = 0
# take opponents maximum frequency guess + 1 if below the threshold, otherwise take 7
def reveng(wallet, history):
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
        if i > th:
            cnt += 1
        if i > 2 * th:
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
def revengsmart(wallet, history):
    z = wins(wallet, history)
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

    return min(wallet, res + 1, 7)


# attempt to troll good strategies by providing horrible data
def scare(wallet, history):
    z = wins(wallet, history)
    if (len(history) <= 3):
        return min(wallet, th)
    res = z[0]

    return min(wallet, res + 1, 8)


def gambler(wallet, history):
    return random.randint(0, wallet)


def low(wallet, history):
    z = wins(wallet, history)

    if (z[0] < wallet and z[1] == 4):
        return z[0] + 1
    return random.randint(0, 3)


def villain(wallet, history):
    return max(wallet - 1, 0)


# Edit me!
def get_strategies():
    """
    Returns a list of strategy functions to use in a tournament.

    In the local tester, all of the strategies will be used as separate bidders in the tournament.
    Note that strategies are tracked by their function name for readability in the results, so 
    adding the same function multiple times will not simulate multiple bidders using the same strategy.

    In the official grader, only the first element of the list will be used as your strategy. 
    """
    strategies = [reveng, vivek_troll00, smartseven, gambler, villain, consrand, atk, consatk, cons, consdest,
                  consrand2, seven, powers, fifth, conspow, tenth, six, eight, seventh, eighth, ninth, smart,
                  five, smarterseven, revengsmart, scare, killreveng, troll, half, low, pluw, risky, calcrisk]

    return strategies
