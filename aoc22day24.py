import time

def addVectors(v1, v2):
    return (v1[0] + v2[0], v1[1] + v2[1])

class Blizzard:
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction
    
    def move(self, walls, width, height):
        newP = addVectors(self.position, self.direction)
        if newP in walls:
            if newP[0] == 0:
                newP = (width-2, newP[1])
            elif newP[0] == width-1:
                newP = (1, newP[1])
            elif newP[1] == 0:
                newP = (newP[0], height-2)
            elif newP[1] == height-1:
                newP = (newP[0], 1)
            else:
                raise Exception("Unexpected wall for blizzard to hit!")
        self.position = newP

def vectorDir(symbol):
    if symbol == '<':
        return (-1, 0)
    elif symbol == '>':
        return (1, 0)
    elif symbol == '^':
        return (0, -1)
    elif symbol == 'v':
        return (0, 1)
    else:
        raise Exception("Unexpected direction symbol!")

def makeMapFromFile():
    file = open('day24input.txt', 'r')
    lines = [line.strip() for line in file.readlines()]
    width = len(lines[0])
    height = len(lines)
    blizzards = []
    walls = set()
    walls.add((1,-1)) # so we can't move up from the start position :)
    walls.add((width-2, height)) # same for end position
    for y in range(height):
        for x in range(width):
            pos = (x, y) # decided not to invert y since we'll never go up above 0
            if lines[y][x] == '#':
                walls.add(pos)
            elif lines[y][x] != '.':
                dir = vectorDir(lines[y][x])
                blizzards.append(Blizzard(pos, dir))
    return (width, height, walls, blizzards)

def incrementBlizzards(blizzards, width, height, walls):
    newBlizzSet = set()
    for bliz in blizzards:
        bliz.move(walls, width, height)
        newBlizzSet.add(bliz.position)
    return newBlizzSet

def getNextMoves(position, blizSet, walls):
    (x,y) = position
    nextPossible = (
        (x, y),
        (x-1, y),
        (x+1, y),
        (x, y-1),
        (x, y+1)
    )
    for p in nextPossible:
        if p not in blizSet and p not in walls:
            yield p

def BFS(start, end, width, height, walls, blizzards):
    positions = set()
    positions.add(start)
    nMinutes = 0
    while end not in positions:
        blizSet = incrementBlizzards(blizzards, width, height, walls)
        newPositions = set()
        for p1 in positions:
            for p2 in getNextMoves(p1, blizSet, walls):
                newPositions.add(p2)
        positions = newPositions
        nMinutes += 1
    return nMinutes

(width, height, walls, blizzards) = makeMapFromFile()
start = (1, 0)
end = (width-2, height-1)

time0 = time.perf_counter()
answer = BFS(start, end, width, height, walls, blizzards)
print("Part 1 Answer = " + str(answer))
time1 = time.perf_counter()
print(f"Done in {time1 - time0:0.4f} seconds")

time0 = time.perf_counter()
answer += BFS(end, start, width, height, walls, blizzards)
answer += BFS(start, end, width, height, walls, blizzards)
print("Part 2 Answer = " + str(answer))
time1 = time.perf_counter()
print(f"Done in {time1 - time0:0.4f} seconds")