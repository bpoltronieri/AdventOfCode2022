file = open('day9input.txt', 'r')
instructions = file.readlines()

def touching(posn1, posn2):
    return abs(posn1[0] - posn2[0]) <= 1 and abs(posn1[1] - posn2[1]) <= 1

def moveKnotOne(dirn, knot):
    if dirn == 'U':
        knot[1] += 1
    elif dirn == 'D':
        knot[1] -= 1
    elif dirn == 'L':
        knot[0] -= 1
    elif dirn == 'R':
        knot[0] += 1
    else:
        raise Exception("Unexpected direction!")

def tailFollowsHead(head, tail):
    if head[0] == tail[0]: # if aligned horizontally or vertically, move tail directly towards head by one
        move = 1 if (head[1] > tail[1]) else -1
        tail[1] += move
    elif head[1] == tail[1]:
        move = 1 if (head[0] > tail[0]) else -1
        tail[0] += move
    else: # move diagonally towards head by one
        move0 = 1 if (head[0] > tail[0]) else -1
        move1 = 1 if (head[1] > tail[1]) else -1
        tail[0] += move0
        tail[1] += move1
    return

def moveRopeOne(dirn, rope):
    head = rope[0]
    moveKnotOne(dirn, head)
    previousKnot = head
    for i in range(len(rope) - 1):
        knot = rope[i+1]
        if not touching(knot, previousKnot):
            tailFollowsHead(previousKnot, knot)
        previousKnot = knot
    return

def simulateRopeMoves(instructions, nKnots):
    """
    Simulates rope moves given by the instructions and returns number of unique 
    positions visited by the tail knot.
    """
    rope = [[0,0] for n in range(nKnots)]
    tail = rope[nKnots-1]
    visited = {tuple(tail)}
    for move in instructions:
        move = move.strip().split()
        (dirn, dist) = (move[0], int(move[1]))
        for i in range(dist):
            moveRopeOne(dirn, rope)
            visited.add(tuple(tail))
    return len(visited)

nVisited = simulateRopeMoves(instructions, 2)
print("Part 1 Answer = " + str(nVisited))
nVisited = simulateRopeMoves(instructions, 10)
print("Part 2 Answer = " + str(nVisited))