"""
Written on my phone on QPython 3L whilst on holiday.
Couldn't figure out Android permissions to open a text file,
so input has to be copy pasted into the console...
"""

def intToYourMove(moveInt):
    if moveInt == 0:
        return 'X'
    elif moveInt == 1:
        return 'Y'
    elif moveInt == 2:
        return 'Z'
    else:
        raise Exception("Unexpected moveInt")

def moveToInt(move):
    if move == 'X' or move == 'A':
        return 0
    elif move == 'Y' or move == 'B':
        return 1
    elif move == 'Z' or move == 'C':
        return 2
    else:
        raise Exception("Unexpected move")

def moveScore(yourMove):
    if yourMove == 'X':
        return 1
    elif yourMove == 'Y':
        return 2
    elif yourMove == 'Z':
        return 3
    else:
        raise Exception("Unexpected yourMove")

def resultScore(game):
    theirMove = moveToInt(game[0])
    yourMove = moveToInt(game[1])
    
    if yourMove == theirMove:
        return 3
    elif yourMove == theirMove + 1 or (yourMove == 0 and theirMove == 2):
        return 6
    else:
        return 0
        
def score(strategy):
    total = 0
    for i in range(len(strategy)):
        total += moveScore(strategy[i][1])
        total += resultScore(strategy[i])
    return total
    

strategy = []
print("Paste your input then enter 'stop'")
x = input()
while x != "stop":
    game = [x[0], x[2]]
    strategy.append(game)
    x = input()

total = score(strategy) 
print("Part 1 Answer = " + str(total))

for i in range(len(strategy)):
    strat = strategy[i][1]
    theirMove = moveToInt(strategy[i][0])
    if strat == 'X':
        newMove = (theirMove - 1) % 3
        strategy[i][1] = intToYourMove(newMove)
    elif strat == 'Y':
        strategy[i][1] = intToYourMove(theirMove)
    elif strat == 'Z':
        newMove = (theirMove + 1) % 3
        strategy[i][1] = intToYourMove(newMove)
    else:
        raise Exception("Unexpected strat")

total = score(strategy)
print("Part 2 Answer = " + str(total))