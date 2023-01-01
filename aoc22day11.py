import math

class Monkey:
    nInspections = 0
    def __init__(self, items, operation, test, monkeyIfTrue, monkeyIfFalse):
        self.items = items
        self.operation = operation
        self.test = test
        self.monkeyIfTrue = monkeyIfTrue
        self.monkeyIfFalse = monkeyIfFalse

def makeMonkeysFromFile():
    """
    Creates array of Monkeys from input file. Returns (monkeys, moduloBy),
    where moduloBy is the number that the item worry levels can be modulod with
    to keep numbers low without affecting the results of any tests.
    
    In practice since the numbers in the "Test: divisible by 7" lines are all primes,
    moduloBy will be the product of the primes. If not prime it would be their LCM.
    """
    monkeys = []
    file = open('day11input.txt', 'r')
    lines = file.readlines()
    i = 0
    divisibles = []
    while i < len(lines):
        items = [int(x) for x in lines[i+1].strip()[16:].split(", ")]
        
        operationString = lines[i+2].strip()[17:] # e.g. "old * 13"
        operation = lambda old, s = operationString : eval(s)
        
        testInt = int(lines[i+3].strip()[19:]) # e.g. integer in "Test: divisible by 19"
        test = lambda x, t = testInt : (x % t) == 0
        divisibles.append(testInt)
        
        monkeyIfTrue = int(lines[i+4].strip()[25:])
        monkeyIfFalse = int(lines[i+5].strip()[26:])
        
        monkeys.append(Monkey(items, operation, test, monkeyIfTrue, monkeyIfFalse))
        
        i += 7 # number of lines per monkey
    
    return (monkeys, math.lcm(*divisibles))

def simulateNRounds(monkeys, N, moduloBy, divideWorryByThree): 
    for round in range(N):
        for monkey in monkeys:
            for item in monkey.items:
                monkey.nInspections += 1
                
                worry = monkey.operation(item)
                if divideWorryByThree:
                    worry = worry // 3
                worry = worry % moduloBy # to keep numbers small without changing result of any tests
                
                if monkey.test(worry):
                    monkeys[monkey.monkeyIfTrue].items.append(worry)
                else:
                    monkeys[monkey.monkeyIfFalse].items.append(worry)
            monkey.items.clear() # all items thrown to other monkeys
    return

(monkeys, moduloBy) = makeMonkeysFromFile()
simulateNRounds(monkeys, 20, moduloBy, divideWorryByThree=True)
monkeys.sort(key=lambda x : x.nInspections, reverse=True)
print("Part 1 Answer = " + str(monkeys[0].nInspections * monkeys[1].nInspections))

(monkeys, moduloBy) = makeMonkeysFromFile()
simulateNRounds(monkeys, 10000, moduloBy, divideWorryByThree=False)
monkeys.sort(key=lambda x : x.nInspections, reverse=True)
print("Part 2 Answer = " + str(monkeys[0].nInspections * monkeys[1].nInspections))