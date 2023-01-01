file = open('day8input.txt', 'r')
lines = file.readlines()
grid = [[int(x) for x in y.strip()] for y in lines]
visibilities = [[False for x in y] for y in lines]

def getVisibilitiesOfLines(grid, visibilities, horizontal, forward):
    grid_size = len(grid)
    for i in range(grid_size):
        tallestVisible = -1
        for j in range(grid_size):
            j = j if forward else (grid_size - 1 - j)
            row = i if horizontal else j
            col = j if horizontal else i
            if grid[row][col] > tallestVisible:
                visibilities[row][col] = True
                tallestVisible = grid[row][col]

def populateVisibilities(grid, visibilities):
    getVisibilitiesOfLines(grid, visibilities, horizontal=True, forward=True)
    getVisibilitiesOfLines(grid, visibilities, horizontal=True, forward=False)
    getVisibilitiesOfLines(grid, visibilities, horizontal=False, forward=True)
    getVisibilitiesOfLines(grid, visibilities, horizontal=False, forward=False)

def withinGrid(i, j, grid_size):
    return i >= 0 and j >= 0 and i < grid_size and j < grid_size

def incrementPosition(i, j, horizontal, forward):
    increment = 1 if forward else -1
    if horizontal:
        i += increment
    else:
        j += increment
    return (i, j)

def viewingDistance(grid, i, j, horizontal, forward):
    viewingDistance = 0
    grid_size = len(grid)
    maxHeight = grid[i][j]
    (i, j) = incrementPosition(i, j, horizontal, forward)
    while withinGrid(i, j, grid_size):
        if grid[i][j] <= maxHeight:
            viewingDistance += 1
        if grid[i][j] >= maxHeight:
            break
        (i, j) = incrementPosition(i, j, horizontal, forward)
    return viewingDistance
             
def getScenicScores(grid, scenicScores):
    grid_size = len(grid)
    for i in range(grid_size):
        for j in range(grid_size):
            scenicScores[i][j] *= viewingDistance(grid, i, j, horizontal=True, forward=True)
            scenicScores[i][j] *= viewingDistance(grid, i, j, horizontal=True, forward=False)
            scenicScores[i][j] *= viewingDistance(grid, i, j, horizontal=False, forward=True)
            scenicScores[i][j] *= viewingDistance(grid, i, j, horizontal=False, forward=False)

populateVisibilities(grid, visibilities)
nVisible = sum(sum(x == True for x in y) for y in visibilities)
print("Part 1 Answer = " + str(nVisible))

scenicScores = [[1 for x in y] for y in lines]
getScenicScores(grid, scenicScores)
topScenicScore = max(max(x) for x in scenicScores)
print("Part 2 Answer = " + str(topScenicScore))