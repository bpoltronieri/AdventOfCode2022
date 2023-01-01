def initStacksAndInstructions(lines):
    nStacks = len(lines[0]) // 4 # each crate has horizontal space for '[X] '
    stacks = [[] for n in range(nStacks)]
    i = 0
    while (lines[i][1] != '1'): # line which contains stack indices 1-9
        for j in range(nStacks):
            crate = lines[i][4*j + 1]
            if (crate != ' '):
                stacks[j].insert(0, crate)
        i += 1
    i += 2 # move to first instruction line
    instructions = []
    while (i < len(lines)):
        instructions.append([int(y) for y in lines[i].strip().replace("move ", ' ').replace(" from ", ' ').replace(" to ", ' ').split()])
        i += 1
    return (stacks, instructions)

def moveNfromAtoB(N, A, B, stacks):
    for i in range(N):
        stacks[B-1].append(stacks[A-1].pop())
        
def moveNfromAtoBandPreserveOrder(N, A, B, stacks):
    lenB = len(stacks[B-1])
    for i in range(N):
        stacks[B-1].insert(lenB, stacks[A-1].pop())
        
def stackMessage(stacks):
    message = ""
    for stack in stacks:
        message += stack[-1]
    return message

file = open('day5input.txt', 'r')
lines = file.readlines()
(stacks, instructions) = initStacksAndInstructions(lines)

for instruction in instructions:
    moveNfromAtoB(*instruction, stacks)
print("Part 1 Answer = " + stackMessage(stacks))

(stacks, instructions) = initStacksAndInstructions(lines)
for instruction in instructions:
    moveNfromAtoBandPreserveOrder(*instruction, stacks)
print("Part 2 Answer = " + stackMessage(stacks))