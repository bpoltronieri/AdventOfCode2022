from collections import deque

file = open('day12input.txt', 'r')
lines = file.readlines()
grid = [[x for x in y.strip()] for y in lines]

def find(grid, char):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (grid[i][j] == char):
                return (i, j)
    return None

start = find(grid, 'S')
end = find(grid, 'E')

def inGrid(grid, x):
    return x[0] >= 0 and x[0] < len(grid) and x[1] >= 0 and x[1] < len(grid[x[0]])

def adjacentGridPositions(grid, current):
    left = (current[0] - 1, current[1])
    right = (current[0] + 1, current[1])
    up = (current[0], current[1] + 1)
    down = (current[0], current[1] - 1)
    adjacents = [left, right, up, down]
    for p in (x for x in adjacents if inGrid(grid, x)):
        yield p

def gridHeight(grid, position):
    char = grid[position[0]][position[1]]
    if (char == 'S'):
        char = 'a'
    elif (char == 'E'):
        char = 'z'
    return ord(char)

def atMostOneHigher(grid, A, B):
    # returns whether we can step from A to B
    return gridHeight(grid, B) <= gridHeight(grid, A) + 1

def BFS(grid, end, start, stopAtFirstA=False):
    # written to walk from end to start to make part two easier, where we need shortest path from end to any 'a'
    queue = deque()
    queue.append((end, 0)) # (position, nSteps)
    visited = {end}
    
    while (len(queue) > 0):
        (position, nSteps) = queue.popleft()
        
        if ((stopAtFirstA and gridHeight(grid, position) == ord('a')) or position == start):
            return nSteps
        
        for next in adjacentGridPositions(grid, position):
            if (next not in visited) and atMostOneHigher(grid, next, position):
                queue.append((next, nSteps + 1))
                visited.add(next)
    
    return None

print("Part 1 Answer = " + str(BFS(grid, end, start)))
print("Part 2 Answer = " + str(BFS(grid, end, start, stopAtFirstA=True)))