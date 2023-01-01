def sign(x):
    return -1 if x < 0 else (0 if x == 0 else 1)

def addStoneLineToMap(caveMap, start, end):
    if (start[0] == end[0]): # vertical line
        i = 0
        dirn = sign(end[1] - start[1])
        while (start[1] + i * dirn != end[1] + dirn):
            caveMap[(start[0], start[1] + i * dirn)] = '#'
            i += 1
    elif (start[1] == end[1]): # horizontal line
        i = 0
        dirn = sign(end[0] - start[0])
        while (start[0] + i * dirn != end[0] + dirn):
            caveMap[(start[0] + i * dirn, start[1])] = '#'
            i += 1
    else:
        raise Exception("Unexpected straight line!")

def buildCaveMapFromFile():
    file = open('day14input.txt', 'r')
    data = [[int(x) for x in line.strip().replace(',', ' ').replace(" -> ", ' ').split()] for line in file.readlines()]
    caveMap = dict()
    maxY = 0
    for path in data:
        i = 0
        while (i + 2 < len(path)):
            start = (path[i], path[i+1])
            end = (path[i+2], path[i+3])
            addStoneLineToMap(caveMap, start, end)
            maxY = max(maxY, max(path[i+1], path[i+3]))
            i += 2
    return (caveMap, maxY)
    
def drawCaveMap(caveMap, fullMap=False):
    # not implemented to draw the infinite floor from part two
    minX = min(p[0] for p in caveMap.keys()) - 1
    maxX = max(p[0] for p in caveMap.keys()) + 1
    minY = min(p[1] for p in caveMap.keys())
    if (fullMap):
        maxY = max(p[1] for p in caveMap.keys()) + 1
    else: # only draw to lowest settled sand plus two, so we can see the stone it settled on
        maxY = max(p[1] for p in caveMap.keys() if caveMap[p] == 'o' or caveMap[p] == '+') + 2
    for i in range(maxY - minY + 1):
        line = []
        for j in range(maxX - minX + 1):
            position = (minX + j, minY + i)
            if position in caveMap:
                line.append(caveMap[position])
            else:
                line.append('.')
        print(''.join(line))

def emptySpace(caveMap, position, withFloor, floorY):
    if (withFloor):
        if position[1] == floorY:
            return False
    return position not in caveMap

def simulateSandFall(caveMap, maxY, withFloor=False):
    if (withFloor):
        maxY += 2
    source = (500, 0)
    caveMap[source] = '+'
    fellIntoAbyss = False
    nSettledSand = 0
    while not fellIntoAbyss and caveMap[source] != 'o':
        # drawCaveMap(caveMap)
        # input()
        current = source
        while current[1] <= maxY:
            below = (current[0], current[1] + 1)
            belowLeft = (current[0] - 1, current[1] + 1)
            belowRight = (current[0] + 1, current[1] + 1)
            if emptySpace(caveMap, below, withFloor, maxY):
                current = below
            elif emptySpace(caveMap, belowLeft, withFloor, maxY):
                current = belowLeft
            elif emptySpace(caveMap, belowRight, withFloor, maxY):
                current = belowRight
            else:
                caveMap[current] = 'o'
                nSettledSand += 1
                break
        if (current[1] > maxY):
            fellIntoAbyss = True
    return nSettledSand

(caveMap, maxY) = buildCaveMapFromFile()
print("Part 1 Answer = " + str(simulateSandFall(caveMap, maxY)))
(caveMap, maxY) = buildCaveMapFromFile()
print("Part 2 Answer = " + str(simulateSandFall(caveMap, maxY, withFloor=True)))