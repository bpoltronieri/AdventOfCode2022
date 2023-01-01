class Monkey:
    def __init__(self, name, value=None, monkey1=None, monkey2=None, operation=None):
        self.name = name
        # when initialised, either value is not None or monkeys and operation aren't None
        self.value = value
        self.monkey1 = monkey1
        self.monkey2 = monkey2
        self.operation = operation
    
    def getValue(self, monkeys):
        if self.value != None:
            return self.value
        value1 = monkeys[self.monkey1].getValue(monkeys)
        value2 = monkeys[self.monkey2].getValue(monkeys)
        result = int(eval(str(value1) + self.operation + str(value2)))

        if self.name == "root":
            print("Value 1 = " + str(value1))
            print("Value 2 = " + str(value2))

        # self.value = result # caching values doesn't actually seem to help
        return result

def makeMonkeysFromFile():
    file = open("day21input.txt")
    monkeys = dict()
    for line in (x.strip().split(": ") for x in file.readlines()):
        name = line[0]
        if line[1][0].isnumeric():
            monkeys[name] = Monkey(name, int(line[1]))
        else:
            op = line[1].split()
            monkeys[name] = Monkey(name, value=None, monkey1 = op[0], monkey2=op[2], operation=op[1])
    return monkeys

monkeys = makeMonkeysFromFile()
answer = monkeys["root"].getValue(monkeys)
print("Part 1 Answer = " + str(answer))

# solved part two by doing a binary search by hand :)
monkeys["root"].operation = "=="
monkeys["humn"].value = 1
while monkeys["root"].getValue(monkeys) != 1:
    v = input("Try a new value: ")
    monkeys["humn"].value = v
print("Part 2 Answer = " + str(monkeys["humn"].value))