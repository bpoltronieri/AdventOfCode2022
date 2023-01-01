file = open('day10input.txt', 'r')
instructions = [x.strip().split() for x in file.readlines()]
XValuesDuringCycles = [1, 1] # X values during each cycle
lastX = 1
for command in instructions:
    if command[0] == "noop":
        XValuesDuringCycles.append(lastX)
    else:
        XValuesDuringCycles.append(lastX)
        lastX += int(command[1])
        XValuesDuringCycles.append(lastX)

def sumOfNCycles(start, increment):
    i = start
    totalSignal = 0
    while (i < len(XValuesDuringCycles)):
        totalSignal += XValuesDuringCycles[i]  * i
        i += increment
    return totalSignal

print("Part 1 Answer = " + str(sumOfNCycles(start=20, increment=40)))

def drawCRT(CRT):
    for row in CRT:
        print(''.join(row))

def spriteOnPixel(col, cycle):
    return abs(col - XValuesDuringCycles[cycle+1]) <= 1

def runCycles(CRT):
    for cycle in range(40 * 6):
        row = cycle // 40
        col = cycle % 40
        if spriteOnPixel(col, cycle):
            CRT[row][col] = '#'
        else:
            CRT[row][col] = ' '

CRT = [[' '] * 40 for i in range(6)]
runCycles(CRT)
drawCRT(CRT)
print("Part 2 Answer = " + "Look at the image above!")