import time
from collections import deque

def getAdjacentNeighbours(cube):
    yield (cube[0] - 1, cube[1], cube[2])
    yield (cube[0] + 1, cube[1], cube[2])
    yield (cube[0], cube[1] - 1, cube[2])
    yield (cube[0], cube[1] + 1, cube[2])
    yield (cube[0], cube[1], cube[2] - 1)
    yield (cube[0], cube[1], cube[2] + 1)

def surfaceArea(voxelSet):
    area = 0
    for cube in voxels:
        for neighbour in getAdjacentNeighbours(cube):
            if neighbour not in voxelSet:
                area += 1
    return area

def inBox(voxel, box):
    return voxel[0] >= box[0] and voxel[0] <= box[3] and voxel[1] >= box[1] and voxel[1] <= box[4] and voxel[2] >= box[2] and voxel[2] <= box[5]

def floodFill(voxelSet, visited, start, boundingBox):
    # flood fills from start. does nothing if we hit void outside box, else adds all newly visited points to voxelSet (i.e. fills the pockets with lava)
    queue = deque()
    newVisited = set()
    visited.add(start)
    newVisited.add(start)
    queue.append(start)
    hitVoid = False
    while len(queue) > 0:
        currentVoxel = queue.popleft()
        
        if not inBox(currentVoxel, boundingBox):
            hitVoid = True
            continue
        
        for neighbour in getAdjacentNeighbours(currentVoxel):
            if neighbour not in visited and neighbour not in voxelSet:
                visited.add(neighbour)
                newVisited.add(neighbour)
                queue.append(neighbour)
    
    if not hitVoid:
        for x in newVisited:
            voxelSet.add(x)

def surfaceAreaWithoutPockets(voxels):
    voxelSet = set(voxels)
    minX = min((x[0] for x in voxels))
    maxX = max((x[0] for x in voxels))
    minY = min((x[1] for x in voxels))
    maxY = max((x[1] for x in voxels))
    minZ = min((x[2] for x in voxels))
    maxZ = max((x[2] for x in voxels))
    boundingBox = (minX, minY, minZ, maxX, maxY, maxZ)
    
    visited = set()
    for x in range(minX, maxX + 1):
        for y in range(minY, maxY + 1):
            for z in range(minZ, maxZ + 1):
                if (x,y,z) not in voxelSet and (x,y,z) not in visited:
                    floodFill(voxelSet, visited, (x,y,z), boundingBox)
    
    return surfaceArea(voxelSet)

file = open('day18input.txt', 'r')
voxels = [eval('(' + line.strip() + ')') for line in file.readlines()]

time0 = time.perf_counter()
print("Part 1 Answer = " + str(surfaceArea(set(voxels))))
time1 = time.perf_counter()
print(f"Done in {time1 - time0:0.4f} seconds")

time0 = time.perf_counter()
print("Part 2 Answer = " + str(surfaceAreaWithoutPockets(voxels)))
time1 = time.perf_counter()
print(f"Done in {time1 - time0:0.4f} seconds")