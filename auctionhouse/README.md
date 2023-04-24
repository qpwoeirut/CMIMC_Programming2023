## Solution

After trying a couple of strategies out, we noticed that a lot of people were betting large amounts initially and then reducing bets over time. We noticed that in the first 5 turns, people were betting >= 10 once or twice (with approximately 70% probability). As a result, we realized that if we bet larger amounts later in the game, we had a higher chance of winning (because other teams would run out of mana quickly). We built our strategy with this in mind, also noting that we needed to make sure to win some initial games (in order to not get eliminated early).

First, we looked through the data and realized that on the first bet, about 18% of people were betting 0 and another 15% were betting 1. We were willing to take this risk on the first bet, so we bet 1 on the first turn. On the second turn, we decided to bet another small amount (if it was the opponents second turn, we assumed we would lose and bet 0, but if it was the opponent's first turn, we took the 25% risk and bet 1 in case we could win that match). 

After the second turn, we tried to capitalize on other team's initial bets, by betting one more than their most recent bet. We realized that this strategy could bankrupt us early on if we came across a team that bet something like 50 initially, so we decided to make our bets at most 16. Additionally, if we reached a later stage in the game where the opponent's most recent bet was greater than the amount that they had left, we bet 1 more than the amount that they had left over (since this guaranteed a win in the game anyway and this way we could conserve our mana).

Our code looked like this:


```py
def wins(wallet, history):
    sm = 100
    l = 0
    for i, j in history:
        sm -= i
        if j == False:
            l += 1
    return sm, l
    
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
```
