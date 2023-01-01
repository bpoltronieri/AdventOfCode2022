import re
import os

def addVectors(v1, v2):
    return (v1[0] + v2[0], v1[1] + v2[1])

# next few functions should probably be in a Map or Cube class

def mapValue(map, position):
    # first apply padding around map:
    if position[1] < 0 or position[1] >= len(map) or position[0] < 0 or position[0] >= len(map[position[1]]):
        return " "
    return map[position[1]][position[0]]

def findFirstNonEmpty(map, start, direction):
    current = start
    while mapValue(map, current) == " ":
        current = addVectors(current, direction)
    return current

def faceOfPosition(position):
    """
        _ _
       |A|B|
      _|C|
     |D|E|
     |F|

    """
    (x,y) = position
    if y // 50 == 0: # first row of faces
        if x  // 50 == 1:
            return 'A'
        else:
            return 'B'
    elif y // 50 == 1: # second row
        return 'C'
    elif y // 50 == 2:
        if x // 50 == 0:
            return 'D'
        else:
            return 'E'
    else:
        return 'F'

L = (-1, 0)
R = (1, 0)
U = (0, -1)
D = (0, 1)

class State:
    # dict mapping (face, dir) to (newFace, newDir, localCoordMapping)
    wrapToFace = {
        ('A', L) : ('D', R, lambda p : (0, 49 - p[1])),       # p => (0, -y)
        ('A', U) : ('F', R, lambda p : (0, p[0])),            # p => (0, x)
        ('B', U) : ('F', U, lambda p : (p[0], 49)),           # p => (x, 49)
        ('B', R) : ('E', L, lambda p : (49, 49 - p[1])),      # p => (49, -y)
        ('B', D) : ('C', L, lambda p : (49, p[0])),           # p => (49, x)
        ('C', L) : ('D', D, lambda p : (p[1], 0)),            # p => (y, 0)
        ('C', R) : ('B', U, lambda p : (p[1], 49)),           # p => (y , 49)
        ('D', L) : ('A', R, lambda p : (0, 49 - p[1])),       # p => (0, -y)
        ('D', U) : ('C', R, lambda p : (0, p[0])),            # p => (0, x)
        ('E', R) : ('B', L, lambda p : (49, 49 - p[1])),      # p => (49, -y)
        ('E', D) : ('F', L, lambda p : (49, p[0])),           # p => (49, x)
        ('F', L) : ('A', D, lambda p : (p[1], 0)),            # p => (y, 0)
        ('F', R) : ('E', U, lambda p : (p[1], 49)),           # p => (y, 49)
        ('F', D) : ('B', D, lambda p : (p[0], 0))             # p => (x, 0)
    }

    def __init__(self, map, position, direction):
        self.map = map
        self.position = position # 2D vector as tuple
        self.direction = direction # 2D unit vector as tuple
    
    def drawMap(self):
        os.system('cls')
        for y in range(len(self.map)):
            line = self.map[y]
            if y == self.position[1]:
                playerChar = None
                if self.direction == L:
                    playerChar = '<'
                elif self.direction == U:
                    playerChar = '^'
                elif self.direction == R:
                    playerChar = '>'
                elif self.direction == D:
                    playerChar = 'v'

                x = self.position[0]
                line = self.map[y][:x] + playerChar + self.map[y][x+1:]
            print(line)
        # input("Press anything to continue")
    
    def localPosition(self):
        # local position within a cube face
        return (self.position[0]%50, self.position[1]%50)
    
    def globalPosition(self, localPosition, face):
        (x, y) = localPosition
        if face == 'A':
            return (50 + x, y)
        elif face == 'B':
            return (100 + x, y)
        elif face == 'C':
            return (50 + x, 50 + y)
        elif face == 'D':
            return (x, 100 + y)
        elif face == 'E':
            return (50 + x, 100 + y)
        elif face == 'F':
            return (x, 150 + y)
    
    def password(self):
        row = self.position[1] + 1
        col = self.position[0] + 1
        facing = None
        if self.direction == (1,0):
            facing = 0
        elif self.direction == (0,1):
            facing = 1
        elif self.direction == (-1,0):
            facing = 2
        elif self.direction == (0,-1):
            facing = 3
        else:
            raise Exception("Unexpected direction")
        return 1000 * row + 4 * col + facing
    
    def rotate(self, rotation):
        # remember that positive y means going down
        if rotation == 'R':
            self.direction = (-self.direction[1], self.direction[0])
        elif rotation == 'L':
            self.direction = (self.direction[1], -self.direction[0])
        else:
            raise Exception("Unexpected rotation")
    
    def wrapAround(self, cube=False):
        wrappedP = None
        wrappedD = self.direction
        if not cube:
            if self.direction[0] == 1: # left-to-right
                wrappedP = (0, self.position[1])
            elif self.direction[0] == -1:
                wrappedP = (len(map[0])-1, self.position[1])
            elif self.direction[1] == 1: # top-to-bottom
                wrappedP = (self.position[0], 0)
            else:
                wrappedP = (self.position[0], len(map)-1)
        else:
            # self.drawMap()
            currentFace = faceOfPosition(self.position)
            currentLocalPosition = self.localPosition()
            (newFace, newDir, localMapping) = State.wrapToFace[(currentFace, self.direction)]
            newLocalPosition = localMapping(currentLocalPosition)
            newGlobalPosition = self.globalPosition(newLocalPosition, newFace)

            wrappedP = newGlobalPosition
            wrappedD = newDir
        return (wrappedP, wrappedD)
    
    def move(self, distance, cube=False):
        for d in range(distance):
            newP = addVectors(self.position, self.direction)
            newD = self.direction

            if mapValue(map, newP) == " ": # wrap around
                (newP, newD) = self.wrapAround(cube)
                if not cube:
                    newP = findFirstNonEmpty(map, newP, newD)

            if mapValue(map, newP) == ".":
                self.position = newP
                self.direction = newD
                # self.drawMap()
            elif mapValue(map, newP) == "#":
                break
    
    def runInstruction(self, instruction, cube=False):
        if instruction[0].isalpha():
            self.rotate(instruction)
            # self.drawMap()
        else:
            self.move(int(instruction), cube)
    
    def runInstructions(self, instructions, cube=False):
        for i in instructions:
            self.runInstruction(i, cube)

def makeMapAndInstructionsFromFile():
    file = open("day22input.txt")
    map = []
    instructions = None
    mapDone = False
    for line in (x.replace("\n", "") for x in file.readlines()):
        if mapDone:
            s = re.split('(\d+)|\[a-zA-Z]', line)
            instructions = s[1:len(s)-1]
        elif line == "":
            mapDone = True
        else:
            map.append(line)
    return (map, instructions)

(map, instructions) = makeMapAndInstructionsFromFile()
startPosition = (map[0].index('.'), 0)
startDirection = (1, 0)

state = State(map, startPosition, startDirection)
state.runInstructions(instructions)
print("Part 1 Answer = " + str(state.password()))

state = State(map, startPosition, startDirection)
state.runInstructions(instructions, cube=True)
print("Part 2 Answer = " + str(state.password()))