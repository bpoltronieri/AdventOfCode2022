def pairContainsPair(pair1, pair2):
    """
    pair1/2 are integer intervals. list of two ints.
    returns whether pair1 fully contains pair2
    """
    return pair1[0] <= pair2[0] and pair1[1] >= pair2[1]
    
def pairsOverlap(pair1, pair2):
    return not (pair1[0] > pair2[1] or pair1[1] < pair2[0])

file = open('day4input.txt', 'r')
pairs = [[int(y) for y in pair] for pair in [x.strip().replace(',', ' ').replace('-', ' ').split() for x in file.readlines()]] # each pair is list of 4 integers [low1, high1, low2, high2]

total = sum((pairContainsPair(pair[0:2], pair[2:]) or pairContainsPair(pair[2:], pair[0:2])) for pair in pairs) 
print("Part 1 Answer = " + str(total))

total = sum(pairsOverlap(pair[0:2], pair[2:]) for pair in pairs)
print("Part 2 Answer = " + str(total))