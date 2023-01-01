def nDistinctCharacters(string):
    return len(set(string))

def findFirstNDistinctMessage(buffer, length):
    answer = -1
    for i in range(len(buffer) - (length-1)):
        if nDistinctCharacters(buffer[i : i+length]) == length:
            answer = i + length
            break
    return answer

file = open('day6input.txt', 'r')
buffer = file.readlines()[0].strip()
print("Part 1 Answer = " + str(findFirstNDistinctMessage(buffer, 4)))
print("Part 2 Answer = " + str(findFirstNDistinctMessage(buffer, 14)))