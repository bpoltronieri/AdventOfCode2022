from functools import cmp_to_key

file = open('day13input.txt', 'r')
packets = [eval(x.strip()) for x in file.readlines() if x != '\n']

def sign(x):
    return -1 if x < 0 else (0 if x == 0 else 1)

def comparePackets(value1, value2):
    # returns -1 if value1 < value2, 0 if value1 == value2, 1 if value1 > value2
    if (type(value1) is int and type(value2) is int):
        return sign(value1 - value2)
    elif (type(value1) is list and type(value2) is list):     
        for i in range(min(len(value1), len(value2))):
            comp = comparePackets(value1[i], value2[i])
            if (comp != 0):
                return comp
        # one or both lists have run out of elements:
        return sign(len(value1) - len(value2))
    elif (type(value1) is int and type(value2) is list):
        return comparePackets([value1], value2)
    elif (type(value1) is list and type(value2) is int):
        return comparePackets(value1, [value2])
    else:
        raise Exception("Unexpected value types!")

def sumOrderedPairIndices(packets):
    total = 0
    for i in range(len(packets)//2):
        if comparePackets(packets[2*i], packets[2*i + 1]) == -1:
            total += (i+1)
    return total

print("Part 1 Answer = " + str(sumOrderedPairIndices(packets)))

divider1 = [[2]]
divider2 = [[6]]
packets.append(divider1)
packets.append(divider2)
packets.sort(key=cmp_to_key(comparePackets))
print("Part 2 Answer = " + str((packets.index(divider1) + 1) * (packets.index(divider2) + 1)))