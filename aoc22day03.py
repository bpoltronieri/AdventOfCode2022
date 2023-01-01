def priority(c):
    if c.islower():
        return ord(c) - ord('a') + 1
    else:
        return ord(c) - ord('A') + 27

file = open('day3input.txt', 'r')
lines = file.readlines()

rucksacks = [] # list of lists of two sets of characters, one for each compartment
for line in lines:
    compartmentSize = (len(line) - 1) // 2 # minus 1 is for /n character
    newRucksack = [set(line[0 : compartmentSize]), set(line[compartmentSize : 2*compartmentSize])]
    rucksacks.append(newRucksack)

total = 0
for rucksack in rucksacks:
    total += priority(set.intersection(*rucksack).pop())

print("Part 1 Answer = " + str(total))

total = 0
for i in range(len(rucksacks)//3):
    groupFullRucksacks = []
    for j in range(3):
        groupFullRucksacks.append(set.union(*rucksacks[3*i + j]))
    total += priority(set.intersection(*groupFullRucksacks).pop())

print("Part 2 Answer = " + str(total))