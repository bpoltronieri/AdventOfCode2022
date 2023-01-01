class State:
    def __init__(self, map, position, direction):
        self.map = map
        self.position = position # 2D vector as tuple
        self.direction = direction # 2D unit vector as tuple

def makeMapFromFile():
    file = open("day23input.txt")
    lines = [x.strip() for x in file.readlines()]
    elves = set()
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            if lines[y][x] == '#':
                elves.add((x, -y))
    return elves

def drawMap(elves):
    minX = min([e[0] for e in elves])
    maxX = max([e[0] for e in elves])
    minY = min([e[1] for e in elves])
    maxY = max([e[1] for e in elves])
    for j in range(maxY - minY + 1):
        line = ""
        y = maxY - j
        for i in range(maxX - minX + 1):
            x = minX + i
            if (x,y) in elves:
                line += '#'
            else:
                line += '.'
        print(line)

def nEmptyTiles(elves):
    minX = min([e[0] for e in elves])
    maxX = max([e[0] for e in elves])
    minY = min([e[1] for e in elves])
    maxY = max([e[1] for e in elves])
    return (maxX - minX + 1) * (maxY - minY + 1) - len(elves)

def incrementCount(dict, key):
    if key in dict:
        dict[key] += 1
    else:
        dict[key] = 1

def getNeighbours(elf):
    (x,y) = elf
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (i == 0 and j == 0):
                continue
            yield (x+i, y+j)

def moveInDirection(elf, direction):
    (x,y) = elf
    if direction == 'N':
        return (x, y+1)
    elif direction == 'S':
        return (x, y-1)
    elif direction == 'W':
        return (x-1, y)
    elif direction == 'E':
        return (x+1, y)
    else:
        raise Exception("Unexpected direction!!")

def canMoveDirection(elf, elves, direction):
    (x,y) = elf
    toCheck = None
    if direction == 'N':
        toCheck = ((x,y+1), (x+1, y+1), (x-1, y+1))
    elif direction == 'S':
        toCheck = ((x, y-1), (x+1, y-1), (x-1, y-1))
    elif direction == 'W':
        toCheck = ((x-1, y), (x-1, y+1), (x-1, y-1))
    elif direction == 'E':
        toCheck = ((x+1, y), (x+1, y+1), (x+1, y-1))
    else:
        raise Exception("Unexpected direction!!")
    for p in toCheck:
        if p in elves:
            return False
    return True

def getMove(elf, elves, directions, dir_i):
    mustMove = False
    for p in getNeighbours(elf):
        if p in elves:
            mustMove = True
            break
    if not mustMove:
        return None # stay where you are
    
    for i in range(len(directions)):
        j = (dir_i + i) % len(directions)
        direction = directions[j]
        if canMoveDirection(elf, elves, direction):
            return moveInDirection(elf, direction)

    return None # wanted to move but was blocked in all dir. impossible?

def runRounds(elves, maxRounds=None):
    directions = ('N', 'S', 'W', 'E')
    dir_i = 0 # start with North, rotates each round
    round = 0
    noElvesMoved = False
    while not (noElvesMoved or (maxRounds != None and round == maxRounds)):
        # drawMap(elves)
        # input()
        noElvesMoved = True
        proposedMoves = dict() # maps elf position to their proposed move position
        proposedMoveCounts = dict() # maps move positions to number of elves wanting to move there

        for elf in elves:
            moveTo = getMove(elf, elves, directions, dir_i)
            if moveTo != None:
                proposedMoves[elf] = moveTo
                incrementCount(proposedMoveCounts, moveTo)
        
        for elf in proposedMoves.keys(): # only elves which are moving
            moveTo = proposedMoves[elf]
            if proposedMoveCounts[moveTo] == 1:
                elves.remove(elf)
                elves.add(moveTo)
                noElvesMoved = False

        dir_i = (dir_i+1) % 4
        round += 1
    return round

elves = makeMapFromFile()
runRounds(elves, maxRounds=10)
answer = nEmptyTiles(elves)
print("Part 1 Answer = " + str(answer))

elves = makeMapFromFile()
nRounds = runRounds(elves)
print("Part 2 Answer = " + str(nRounds))