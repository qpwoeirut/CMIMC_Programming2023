"""
Edit this file! This is the file you will submit.
"""
import random

# Implement me!
# 2 example strategies to use in your tournament.


th = 10

def wins(wallet, history):
    sm = 100
    l = 0
    for i, j in history:
        sm -= i
        if j == False:
            l += 1
    return sm, l


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


#attack whenever possible
def atk(wallet, history):
    z = wins(wallet, history)
    return min(wallet, z[0] + 1)

#random under threshold
def consrand(wallet, history):
    return min(wallet, random.randint(0, th))

#random under threshold but above 5
def consrand2(wallet, history):
    return min(wallet, random.randint(th/2, th))

#powers of 2
def powers(wallet, history):
    z = len(history)
    return min(wallet, pow(2,z))

#bet 1/5 each time
def fifth(wallet, history):
    return wallet/5

#bet 1/7 each time
def seventh(wallet, history):
    return wallet/7

#bet 1/8 each time
def eighth(wallet, history):
    return wallet/8

#bet 1/6 each time
def sixth(wallet, history):
    return wallet/6

#bet 1/9 each time
def ninth(wallet, history):
    return wallet/9

def tenth(wallet, history):
    return wallet/10

#powers of 2 but no more than 15
def conspow(wallet, history):
    z = len(history)
    return min(wallet, 20, pow(2,z))

#always guess 7
def seven(wallet, history):
    return min(wallet, 7)

def six(wallet, history):
    return min(wallet, 6)


def eight(wallet, history):
    return min(wallet, 8)

#randomish strategy
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

#bet seven + hope some other things work
def smarterseven(wallet, history):
    z = wins(wallet, history)

    if (z[1] == 4 and z[0] > 7):
        return min(wallet, random.randint(0,th))

    return min(wallet, z[0] + 1, 7)

#bet seven + hope some other things work
def smartseven(wallet, history):
    z = wins(wallet, history)

    return min(wallet, z[0] + 1, 7)

def five(wallet, history):
    z = wins(wallet, history)

    return min(wallet, 5)

#take opponents maximum frequency guess + 1 if below the threshold, otherwise take 7
def reveng (wallet, history):
    z = wins(wallet, history)
    res = 100
    guess = []
    for i,j in history:
        guess.append(i)
    sz = len(guess)
    if (sz > 0):
        res = max(set(guess), key=guess.count)

    if (sz == 2 and guess.count(res) == 2 and guess[0] >= 2 * th):
        return 0
    if (sz == 0):
        return min(wallet, random.randint(0, 5))
    res = min(res, z[0])
    if (wallet >= res + 1 and res + 1 <= th):
        return res + 1
    return min(wallet, res + 1, 7)

#troll bot from LIT server
def vivek_troll00(wallet, history):
  if len(history) <= 0:
    return min(random.randint(6, 7), wallet)
  if history[0][0] < 4:
    return min(history[0][0]+1, wallet)
  return min(random.randint(6, 7), wallet)

def revengsmart (wallet, history):
    z = wins(wallet, history)
    res = 100
    guess = []
    for i,j in history:
        guess.append(i)
    sz = len(guess)
    if (sz > 0):
        res = max(set(guess), key=guess.count)
    res = min(res, z[0])
    if guess.count(res) >= sz/3 and wallet >= res + 1 and res + 1 <= th:
        return res + 1

    return min(wallet, res + 1, 7)

def scare(wallet, history):
    z = wins(wallet, history)
    if (len(history) <= 3):
        return min(wallet, th)
    res = z[0]



    return min(wallet, res + 1, 8)

def gambler(wallet, history):
    return random.randint(0, wallet)

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
    strategies = [reveng, smartseven, gambler, villain, consrand, atk, consatk, cons, consdest,
                  consrand2, seven, powers, fifth, conspow, tenth, six, eight, seventh, eighth, ninth, smart, five, smarterseven, revengsmart, scare]



    return strategies
