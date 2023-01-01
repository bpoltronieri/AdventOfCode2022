import time
import os

class Map:   
    def __init__(self):
        self.settledRocks = set()
        self.highestRock = 0
        pass
    
    def emptySpace(self, position):
        return position[0] > 0 and position[0] < 8 and position[1] > 0 and position not in self.settledRocks
    
    def emptySpaces(self, positions):
        for p in positions:
            if not self.emptySpace(p):
                return False
        return True
    
    def markSettled(self, position):
        if position in self.settledRocks:
            raise Exception("Rock being settled on top of rock!!")
        
        self.settledRocks.add(position)
        self.highestRock = max(self.highestRock, position[1])
    
    def draw(self):
        os.system('cls') # clear screen
        for line in range(1, min(200, self.highestRock + 2)):
            y = self.highestRock + 2 - line
            s = ''
            for x in range(1, 8):
                if (x, y) in self.settledRocks:
                    s += '#'
                else:
                    s += '.'
            s = str(y) + ' |' + s + '|'
            print(s.zfill(20))
        if self.highestRock + 2 <= 200:
            bottomLine = "00000000000+-------+"
            print(bottomLine)
        # time.sleep(0.5)
        x = input()

class Rock:
    def __init__(self, type, map):
        self.type = type # one of '-' '+' 'L' '|' '-'
        
        positionX = 3 # left wall is 0, then two empty spaces
        bottomEdgeY = map.highestRock + 4
        positionY = bottomEdgeY
        if type == '+':
            positionY += 1 # because bottom # of cross sticks out
        
        self.position = (positionX, positionY) # position of leftmost point. the point with two empty spaces to its left. the lowest such point for '|' and '#' where there's a choice
    
    def markSettledOnMap(self, map):
        positions = [] # positions that rock occupies
        positions.append(self.position) # all rock types have this
        
        if self.type == '-':
            positions.append((self.position[0] + 1, self.position[1]))
            positions.append((self.position[0] + 2, self.position[1]))
            positions.append((self.position[0] + 3, self.position[1]))
        elif self.type == '+':
            positions.append((self.position[0] + 1, self.position[1]))
            positions.append((self.position[0] + 2, self.position[1]))
            positions.append((self.position[0] + 1, self.position[1] + 1))
            positions.append((self.position[0] + 1, self.position[1] - 1))
        elif self.type == 'L':
            positions.append((self.position[0] + 1, self.position[1]))
            positions.append((self.position[0] + 2, self.position[1]))
            positions.append((self.position[0] + 2, self.position[1] + 1))
            positions.append((self.position[0] + 2, self.position[1] + 2))
        elif self.type == '|':
            positions.append((self.position[0], self.position[1] + 1))
            positions.append((self.position[0], self.position[1] + 2))
            positions.append((self.position[0], self.position[1] + 3))
        elif self.type == '#':
            positions.append((self.position[0], self.position[1] + 1))
            positions.append((self.position[0] + 1, self.position[1]))
            positions.append((self.position[0] + 1, self.position[1] + 1))
        
        for p in positions:
            map.markSettled(p)
    
    def canMoveDown(self, map):
        newPositions = [] # new positions that would be occupied below rock
        newPositions.append((self.position[0], self.position[1] - 1)) # all rock types have this one
        
        if self.type == '-':
            newPositions.append((self.position[0] + 1, self.position[1] - 1))
            newPositions.append((self.position[0] + 2, self.position[1] - 1))
            newPositions.append((self.position[0] + 3, self.position[1] - 1))
        elif self.type == '+':
            newPositions.append((self.position[0] + 1, self.position[1] - 2))
            newPositions.append((self.position[0] + 2, self.position[1] - 1))
        elif self.type == 'L':
            newPositions.append((self.position[0] + 1, self.position[1] - 1))
            newPositions.append((self.position[0] + 2, self.position[1] - 1))
        elif self.type == '|':
            pass # only the one already added
        elif self.type ==  '#':
            newPositions.append((self.position[0] + 1, self.position[1] - 1))
        
        return map.emptySpaces(newPositions)
    
    def canMoveLeft(self, map):
        newPositions = [] # new positions that would be occupied to left of rock
        newPositions.append((self.position[0] - 1, self.position[1])) # all rock types have this one
        
        if self.type == '-':
            pass # only the one already added
        if self.type == '+':
            newPositions.append((self.position[0], self.position[1] - 1))
            newPositions.append((self.position[0], self.position[1] + 1))
        elif self.type == 'L':
            newPositions.append((self.position[0] + 1, self.position[1] + 1))
            newPositions.append((self.position[0] + 1, self.position[1] + 2))
        elif self.type == '|':
            newPositions.append((self.position[0] - 1, self.position[1] + 1))
            newPositions.append((self.position[0] - 1, self.position[1] + 2))
            newPositions.append((self.position[0] - 1, self.position[1] + 3))
        elif self.type ==  '#':
            newPositions.append((self.position[0] - 1, self.position[1] + 1))
            
        return map.emptySpaces(newPositions)
    
    def canMoveRight(self, map):
        newPositions = [] # new positions that would be occupied to right of rock
        
        if self.type == '-':
            newPositions.append((self.position[0] + 4, self.position[1]))
        elif self.type == '+':
            newPositions.append((self.position[0] + 3, self.position[1]))
            newPositions.append((self.position[0] + 2, self.position[1] - 1))
            newPositions.append((self.position[0] + 2, self.position[1] + 1))
        elif self.type == 'L':
            newPositions.append((self.position[0] + 3, self.position[1]))
            newPositions.append((self.position[0] + 3, self.position[1] + 1))
            newPositions.append((self.position[0] + 3, self.position[1] + 2))
        elif self.type == '|':
            newPositions.append((self.position[0] + 1, self.position[1]))
            newPositions.append((self.position[0] + 1, self.position[1] + 1))
            newPositions.append((self.position[0] + 1, self.position[1] + 2))
            newPositions.append((self.position[0] + 1, self.position[1] + 3))
        elif self.type ==  '#':
            newPositions.append((self.position[0] + 2, self.position[1]))
            newPositions.append((self.position[0] + 2, self.position[1] + 1))
        
        return map.emptySpaces(newPositions)
    
    def applyMove(self, map, move):
        if move == '<' and self.canMoveLeft(map):
            self.position = (self.position[0] - 1, self.position[1])
        elif move == '>' and self.canMoveRight(map):
            self.position = (self.position[0] + 1, self.position[1])
    
    def moveDown(self):
        self.position = (self.position[0], self.position[1] - 1)

def rockHeightAfterNRocks(map, moves, N):
    rockTypes = ('-', '+', 'L', '|', '#')
    nSettledRocks = 0
    r = 0 # rock type index
    m = 0 # move index
    previousStates = dict()
    cycleLength = None # until we find a cycle
    cycleHeight = None
    lastHeight = None
    cycleCount = 0
    
    while (nSettledRocks < N):
        remainingRocks = N - nSettledRocks
        
        if cycleLength == None: # check for cycle
            state = (m, r) # really this should include some info 
            if state in previousStates:
                cycleLength = nSettledRocks - previousStates[state]
                if remainingRocks % cycleLength != 0:
                    cycleLength = None # wait for a better one, which luckily happens to be the correct cycle for my input
                else:
                    print("Cycle from " + str(previousStates[state]) + " to " + str(nSettledRocks))
                    lastHeight = map.highestRock # record height so we know height of cycle
            else:
                previousStates[state] = nSettledRocks
        elif remainingRocks % cycleLength == 0: # we've gone 1 cycle since we first identified a cycle
            cycleHeight = map.highestRock - lastHeight
            return map.highestRock + (remainingRocks//cycleLength) * cycleHeight
        
        newRock = Rock(rockTypes[r], map)
        settled = False
        while not settled:
            newRock.applyMove(map, moves[m])
            if newRock.canMoveDown(map):
                newRock.moveDown()
            else:
                settled = True
                newRock.markSettledOnMap(map)
                nSettledRocks += 1
            m = (m+1) % len(moves)
        r = (r+1) % len(rockTypes)
    
    return map.highestRock

file = open('day17input.txt', 'r')
moves = file.readline().strip()

map = Map()
time0 = time.perf_counter()
print("Part 1 Answer = " + str(rockHeightAfterNRocks(map, moves, 2022)))
time1 = time.perf_counter()
print(f"Done in {time1 - time0:0.4f} seconds")

map = Map()
time0 = time.perf_counter()
print("Part 2 Answer = " + str(rockHeightAfterNRocks(map, moves, 1000000000000)))
time1 = time.perf_counter()
print(f"Done in {time1 - time0:0.4f} seconds")