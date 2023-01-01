import time

class Node:
    def __init__(self, value, previous, next):
        self.value = value
        self.previous = previous
        self.next = next
    
    def toList(self):
        nodes = [self]
        current = self.next
        while (current != self):
            nodes.append(current)
            current = current.next
        return nodes
    
    def print(self):
        values = [self.value]
        current = self.next
        while (current != self):
            values.append(current.value)
            current = current.next
        print(values)
    
    def moveByValue(self, nNodes):
        value = self.value
        
        # trying to be clever below but it breaks things...
        if value >= 0:
            value = (self.value % (nNodes-1))
        else:
            value = ((self.value % (nNodes-1)) - (nNodes-1))
        
        if value == 0:
            return # nothing to do
        
        # remove self from current spot:
        self.previous.next = self.next
        self.next.previous = self.previous
        
        count = 0
        other = self
        while count < abs(value):
            other = other.next if value > 0 else other.previous
            count += 1
        
        # then move self:
        if value > 0: # insert after other
            self.previous = other
            self.next = other.next
            other.next.previous = self
            other.next = self
        else: #insert before other
            self.previous = other.previous
            self.next = other
            other.previous.next = self
            other.previous = self

def makeLinkedListFromFile(decryptionKey=1):
    file = open('day20input.txt', 'r')
    data = [int(line.strip()) for line in file.readlines()]
    
    previous = None
    current = None
    first = None
    for i in range(len(data)):
        current = Node(data[i] * decryptionKey, previous, None)
        if (previous != None):
            previous.next = current
        if i == 0:
            first = current
        previous = current
    first.previous = current
    current.next = first
    return (first, len(data))

def mixDataNTimes(head, nNodes, N):
    toDo = head.toList()
    for i in range(N):
        for x in toDo:
            x.moveByValue(nNodes)
            # head.print()

def sumOf1000thAfterZero(head):
    current = head
    # find zero
    while (current.value != 0):
        current = current.next
    
    current = current.next
    count = 1
    total = 0
    while (count <= 3000):
        if count == 1000 or count == 2000 or count == 3000:
            total += current.value
        count += 1
        current = current.next
    return total

(head, nNodes) = makeLinkedListFromFile()
time0 = time.perf_counter()
mixDataNTimes(head, nNodes, 1)
answer = sumOf1000thAfterZero(head)
print("Part 1 Answer = " + str(answer))
time1 = time.perf_counter()
print(f"Done in {time1 - time0:0.4f} seconds")

(head, nNodes) = makeLinkedListFromFile(decryptionKey=811589153)
time0 = time.perf_counter()
mixDataNTimes(head, nNodes, 10)
answer = sumOf1000thAfterZero(head)
print("Part 2 Answer = " + str(answer))
time1 = time.perf_counter()
print(f"Done in {time1 - time0:0.4f} seconds")