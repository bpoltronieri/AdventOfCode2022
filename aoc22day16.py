from collections import deque
import time

class Valve:
    on = False
    def __init__(self, name, flowRate, tunnels):
        self.name = name
        self.flowRate = flowRate
        self.tunnels = tunnels
        
        if flowRate == 0:
            self.on = True # pretend these are already on, makes rest of code easier

def createValvesFromFile():
    # returns lookup dict mapping valve names to valve objects
    valveLookup = dict()
    file = open('day16input.txt', 'r')
    data = [[x for x in line.strip().replace("Valve ", '').replace("has flow rate=", '').replace("; tunnels lead to valves", ' ').replace("; tunnel leads to valve", ' ').replace(',', '').split()] for line in file.readlines()]
    for line in data:
        newValve = Valve(line[0], int(line[1]), tuple(line[2:]))
        valveLookup[newValve.name] = newValve
    return valveLookup

def BFS(valves, start, end):
    queue = deque()
    queue.append((start, start)) # (position, pathSoFar)
    visited = {start}
    
    while len(queue) > 0:
        (position, path) = queue.popleft()
        
        if position == end:
            return path
        
        for next in (x for x in valves[position].tunnels if x not in visited):
            queue.append((next, path+next))
            visited.add(next)
    
    return None

def fastestPathAtoB(valves, A, B, cache):
    if A+B in cache:
        return cache[A+B]
    else:
        fastestPath = BFS(valves, A, B)
        cache[A+B] = fastestPath
        return fastestPath

def upperBound(timeLeft, nClosedValves, pressureReleased):
    maxFlowRate = 24 # hardcoded
    nValvesToOpen = min(timeLeft, nClosedValves)
    return pressureReleased + (timeLeft-1) * nValvesToOpen * maxFlowRate

def findMaxPressureReleaseDFS(valves, pathCache, position, timeLeft, pressureReleased=0, maxPressure=0):
    closedValves = [v for v in valves if not valves[v].on]
    if len(closedValves) == 0 or timeLeft == 1: # in 1 minute we can open a valve but it won't release any pressure in time
        return max(pressureReleased, maxPressure)
    elif upperBound(timeLeft, len(closedValves), pressureReleased) <= maxPressure:
        return -1 # this run can't achieve better than a path we already found
    
    noTimeForMoreValves = True
    
    for valve in closedValves:
        path = fastestPathAtoB(valves, position, valve, pathCache)
        nSteps = (len(path) // 2) - 1 # divide by 2 because each valve is two characters, -1 to not count start position
        newTimeLeft = timeLeft - nSteps - 1 # -1 for time to open valve
        
        if newTimeLeft > 0:
            valves[valve].on = True
            newPressure = pressureReleased + (newTimeLeft * valves[valve].flowRate)
            noTimeForMoreValves = False
            maxPressure = max(maxPressure, findMaxPressureReleaseDFS(valves, pathCache, valve, newTimeLeft, newPressure, maxPressure))
            valves[valve].on = False # revert to previous state
    
    if noTimeForMoreValves:
        return max(maxPressure, pressureReleased)
    
    return maxPressure

def biPartitions(list):
    nBiPartitions = 2**len(list)
    for i in range(1, nBiPartitions - 1):
        binString = bin(i)[2:].zfill(len(list))
        list1 = [x for x in list if binString[list.index(x)] == '0']
        list2 = [x for x in list if binString[list.index(x)] == '1']
        yield (list1, list2)

def openValves(valves, toOpen):
    for v in toOpen:
        valves[v].on = True

def closeValves(valves, toClose):
    for v in (x for x in toClose if valves[x].flowRate > 0):
        valves[v].on = False

def findMaxPressureReleaseTwoPlayers(valves, pathCache, position, timeLeft):
    maxPressure = 0
    closedValves = [v for v in valves if not valves[v].on]
    
    nPartitions = 2**len(closedValves) - 2
    done = 0
    
    for partition in biPartitions(closedValves):
        done += 1
        if (done % 100 == 0):
            print("Starting partition " + str(done) + " / " + str(nPartitions))
        
        valves1 = partition[0]
        valves2 = partition[1]
        
        # get max pressure that player 1 can release
        openValves(valves, valves2) # so player 1 won't try to open player 2's valves
        pressureReleased = findMaxPressureReleaseDFS(valves, pathCache, position, timeLeft)
        closeValves(valves, valves2)
        
        # get max pressure that player 2 can release
        openValves(valves, valves1)
        pressureReleased += findMaxPressureReleaseDFS(valves, pathCache, position, timeLeft)
        closeValves(valves, valves1)
        
        maxPressure = max(maxPressure, pressureReleased)
    
    return maxPressure

valves = createValvesFromFile()
pathCache = dict()

time0 = time.perf_counter()
print("Part 1 Answer = " + str(findMaxPressureReleaseDFS(valves, pathCache, position="AA", timeLeft=30)))
time1 = time.perf_counter()
print(f"Done in {time1 - time0:0.4f} seconds")

time0 = time.perf_counter()
print("Part 2 Answer = " + str(findMaxPressureReleaseTwoPlayers(valves,pathCache, position="AA", timeLeft=26)))
time1 = time.perf_counter()
print(f"Done in {time1 - time0:0.4f} seconds")