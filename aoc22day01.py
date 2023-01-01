"""
Written on my phone on QPython 3L whilst on holiday.
Couldn't figure out Android permissions to open a text file,
so input has to be copy pasted into the console...
"""

data = []
calories = []
print("Paste your input then enter 'stop'")
x = input()
while x != "stop":
    if x == '':
        data.append(calories)
        calories = []
    else:
        calories.append(int(x))
    x = input()
if len(calories) > 0:
    data.append(calories)

maxCal = 0
for i in range(len(data)):
    cals = sum(data[i])
    if cals > maxCal:
        maxCal = cals
 
print("Part 1 Answer = " + str(maxCal))

topThree = [sum(data[0]), sum(data[1]), sum(data[2])]
topThree.sort()

for i in range(len(data) - 3):
    x = sum(data[i+3])
    if (x > topThree[0]):
        topThree.pop(0)
        topThree.append(x)
        topThree.sort()

print("Part 2 Answer = " + str(sum(topThree)))