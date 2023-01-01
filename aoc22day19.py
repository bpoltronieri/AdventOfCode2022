import time

class State():
    def __init__(self, timeLeft):
        self.nRobots = [1, 0, 0, 0] # [ore, clay, obsidian, geode]
        self.currentlyMakingRobot = [False, False, False, False] # [ore, clay, obsidian, geode]
        self.resources = [0, 0, 0, 0] # [ore, clay, obsidian, geodes]
        self.timeLeft = timeLeft
    
    def copy(self):
        newState = State(self.timeLeft)
        newState.nRobots = self.nRobots.copy()
        newState.currentlyMakingRobot = self.currentlyMakingRobot.copy()
        newState.resources = self.resources.copy()
        return newState
    
    def nGeodes(self):
        return self.resources[3]
    
    def nGuaranteedGeodes(self):
        return self.nGeodes() + self.timeLeft * self.nRobots[3]
    
    def updateOneMinute(self):
        for i in range(4):
            self.resources[i] += self.nRobots[i]
        
        for i in range(4):
            if self.currentlyMakingRobot[i]:
                self.nRobots[i] += 1
                self.currentlyMakingRobot[i] = False
        
        self.timeLeft -= 1
    
    def canAffordRobot(self, type, blueprint):
        for i in range(3):
            if self.resources[i] < blueprint.robotCosts[type][i]:
                return False
        return True
    
    def startMakingRobot(self, type, blueprint):
        for i in range(3):
            self.resources[i] -= blueprint.robotCosts[type][i]
        self.currentlyMakingRobot[type] = True
    
    def possibleNextStates(self, blueprint):
        nextStates = []
             
        # if we have enough robots of a certain type to pay for any other robot type every minute, stop building that type
        considerBuying = [False, False, False, True] # ore, clay, obsidian, geode
        for i in range(3):
            for c in blueprint.robotCosts:
                if self.nRobots[i] < c[i]:
                    considerBuying[i] = True
                    break
        
        canBuyAll = True
        # otherwise consider either obsidian, clay robot, ore robot, or saving up:
        for i in range(4):
            robotType = 3 - i # prioritise more expensive robots
            
            if not considerBuying[robotType]:
                continue
            
            if self.canAffordRobot(robotType, blueprint):
                newState = self.copy()
                newState.startMakingRobot(robotType, blueprint)
                newState.updateOneMinute()
                nextStates.append(newState)
            else:
                canBuyAll = False
        
        # also try saving up, but only if there's something we can't buy:
        if not canBuyAll:
            next = self.copy()
            next.updateOneMinute()
            nextStates.append(next)
        
        return nextStates
    
    def cacheHash(self):
        return (tuple(self.nRobots[:4]), tuple(self.resources[:4]), self.timeLeft)
    
    def upperbound(self):
        # upper bound of number of geodes we can hope to make, even if we made 1 geode robot every minute left
        N = self.timeLeft
        return self.nGuaranteedGeodes() + (N * (N-1))//2
    
    def jettisonResources(self, blueprint):
        # jettison resources we can't spend in time left
        # gives the wrong answer for part 2
        considerBuying = [False, False, False, True] # false if will never buy this robot again
        for i in range(3):
            for c in blueprint.robotCosts:
                if self.nRobots[i] < c[i]:
                    considerBuying[i] = True
                    break
        
        for resource in range(3):
            maxCost = 0 # most we'll ever spend of this resource per minute
            for j in range(4):
                c = blueprint.robotCosts[j]
                maxCost = max(maxCost, c[resource])
            
            if not considerBuying[resource]:
                self.resources[resource] = min(maxCost, self.resources[resource])
            else:
                self.resources[resource] = min((maxCost - self.nRobots[resource])*(self.timeLeft + 1), self.resources[resource])
    
    def maxGeodes(self, blueprint, cache):
        blueprint.nStatesVisited += 1
        
        if self.timeLeft == 0:
            blueprint.maxSoFar = max(blueprint.maxSoFar, self.nGeodes())
            return self.nGeodes()
        if self.upperbound() <= blueprint.maxSoFar:
            return 0
        
        # self.jettisonResources(blueprint) # doesn't work in current state
        
        ch = self.cacheHash()
        if ch in cache:
            blueprint.cacheHit += 1
            return cache[ch]
        
        maxGeodes = self.nGuaranteedGeodes()
        for next in self.possibleNextStates(blueprint):
            nextMax = next.maxGeodes(blueprint, cache)
            maxGeodes = max(maxGeodes, nextMax)
        
        cache[ch] = maxGeodes
        return maxGeodes

class Blueprint():
    def __init__(self, data):
        self.ID = data[0]
        self.robotCosts = ((data[1], 0, 0), (data[2], 0, 0), (data[3], data[4], 0), (data[5], 0, data[6]))
        self.maxSoFar = 0
        self.nStatesVisited = 0
        self.cacheHit = 0
    
    def maxGeodesInNMinutes(self, N):
        startState = State(N)
        self.maxSoFar = 0
        return startState.maxGeodes(blueprint=self, cache=dict())
    
    def qualityLevel(self):
        qualityLevel = self.ID * self.maxGeodesInNMinutes(24)
        print("Done blueprint " + str(self.ID) + ". Quality Level = " + str(qualityLevel))
        # print("Number of states visited " + str(self.nStatesVisited))
        # print("Cache Hit Rate " + str(100 * self.cacheHit / self.nStatesVisited) + "%")
        return qualityLevel

def makeBlueprintsFromFile():
    file = open('day19input.txt', 'r')
    data = [[int(x) for x in line.strip().replace("Blueprint ", '').replace(": Each ore robot costs", '').replace(" ore. Each clay robot costs", '').replace(" ore. Each obsidian robot costs", '').replace(" ore and", '').replace(" clay. Each geode robot costs", '').replace(" obsidian.", '').split()] for line in file.readlines()]
    return [Blueprint(x) for x in data]

blueprints = makeBlueprintsFromFile()

time0 = time.perf_counter()
print("Part 1 Answer = " + str(sum([x.qualityLevel() for x in blueprints])))
time1 = time.perf_counter()
print(f"Done in {time1 - time0:0.4f} seconds")

time0 = time.perf_counter()
answer = 1
for i in range(3):
    answer *= blueprints[i].maxGeodesInNMinutes(32)
    print("Done blueprint " + str(blueprints[i].ID))
print("Part 2 Answer = " + str(answer))
time1 = time.perf_counter()
print(f"Done in {time1 - time0:0.4f} seconds")