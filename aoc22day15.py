def sign(x):
    return -1 if x < 0 else (0 if x == 0 else 1)

def manhattanDist(p1, p2):
    return abs(p2[1]-p1[1]) + abs(p2[0]-p1[0])

def buildSensorReportFromFile():
    """
    Returns dictionary mapping beacon positions to their nearest sensor's position.
    """
    file = open('day15input.txt', 'r')
    data = [[int(x) for x in line.strip().replace("Sensor at x=", '').replace(", y=", ' ').replace(": closest beacon is at x=", ' ').split()] for line in file.readlines()]
    sensorReport = dict()
    for sensor in data:
        sensorPosition = (sensor[0], sensor[1])
        beaconPosition = (sensor[2], sensor[3])
        sensorReport[sensorPosition] = beaconPosition
    return sensorReport

def nEmptySpacesOnLine(sensorReport, y):
    """
    Returns number of spaces on line of height y which definitely don't contain beacons.
    """
    emptySpaces = set()
    for sensor in sensorReport.keys():
        beacon = sensorReport[sensor]
        dist = manhattanDist(sensor, beacon)
        lineHalfLen = dist - abs(y - sensor[1]) # half length of overlap of line y and beacon's area
        
        if (lineHalfLen < 0): # beacon area doesn't overlap with line y
            continue
        
        emptySpaces.add(sensor[0]) # this could be same position as sensor, but still can't be a beacon
        for i in range(lineHalfLen):
            emptySpaces.add(sensor[0] - (i+1))
            emptySpaces.add(sensor[0] + (i+1))
        if beacon[1] == y:
            emptySpaces.remove(beacon[0])
    
    return len(emptySpaces)
    
def touching(interval1, interval2):
    # returns whether intervals overlap or touch at an end
    return (interval2[0] <= interval1[1] + 1 and interval2[0] >= interval1[0]) or (interval1[0] <= interval2[1] + 1 and interval1[0] >= interval2[0])

def addIntervalToLine(lines, line_index, newInterval):
    """
    Given a line, which is a sorted list of non-overlapping intervals (a, b) where the beacon 
    COULD be (including a and b), and an interval (c, d) where the beacon definitely is NOT, 
    adjust the list accordingly.
    """
    line = lines[line_index]
          
    # instert newInterval into line sorted by interval start
    i = 0
    while i < len(line) and line[i][0] < newInterval[0]:
        i+= 1
    line.insert(i, newInterval)
    
    if len(line) > 1: #merge overlapping intervals 
        newLine = []
        i = 0
        while i < len(line):
            currentInterval = list(line[i])
            i += 1
            while i < len(line) and touching(currentInterval, line[i]):
                currentInterval[1] = max(currentInterval[1], line[i][1])
                i += 1
            newLine.append(tuple(currentInterval))
        lines[line_index] = newLine
    
    return

def findDistressBeacon(sensorReport, maxXY):
    # create a list of lines, where each line contains a list of x intervals where beacon
    # definitely CANNOT be. Therefore each list starts as empty
    horizontalLines = [[] for i in range(maxXY + 1)]
    
    nDone = 0
    for sensor in sensorReport.keys():
        nDone += 1
        print("Starting beacon " + str(nDone) + " / " + str(len(sensorReport)))        
        
        beacon = sensorReport[sensor]
        dist = manhattanDist(sensor, beacon)
        
        yStart = max(0, sensor[1] - dist)
        yEnd = min(maxXY, sensor[1] + dist)
        
        if (yEnd < yStart): # if y interval doesn't overlap with (0, maxXY) interval
            continue
        
        for y in range(yStart, yEnd + 1):
            xIntervalHalfLen = dist - abs(y - sensor[1])
            
            xStart = max(0, sensor[0] - xIntervalHalfLen)
            xEnd = min(maxXY, sensor[0] + xIntervalHalfLen)
            xInterval = (xStart, xEnd)
            addIntervalToLine(horizontalLines, y, xInterval)
    
    # now look for only line where we haven't ruled out the entire interval:
    for y in range(len(horizontalLines)):
        line = horizontalLines[y]
        if len(line) == 1 and line[0] == (0, maxXY):
            continue
        x = line[0][1] + 1
        return (x, y)
    
    return (-1,-1)

sensorReport = buildSensorReportFromFile()
print("Part 1 Answer = " + str(nEmptySpacesOnLine(sensorReport, y=2000000)))

maxXY = 4000000
distressBeacon = findDistressBeacon(sensorReport, maxXY)
print("Part 2 Answer = " + str(distressBeacon[0] * 4000000 + distressBeacon[1]))