import time

def snafuToDecimal(snafu):
    decimal = 0
    i = len(snafu) - 1
    for c in snafu:
        if c == '=':
            v = -2
        elif c == '-':
            v = -1
        else:
            v = int(c)
        value = (5**i) * v
        decimal += int(value)
        i -= 1
    return decimal

def decimalToSnafu(decimal):
    i = 0
    while decimal > 5**i:
        i += 1
    answer = ["0"] * (i+1)
    
    j = 0
    while decimal > 0:
        x = decimal % 5
        currentJ = int(answer[j])
        newJ = currentJ + x
        if newJ <= 2:
            answer[j] = str(newJ)
        elif newJ == 3:
            answer[j] = '='
            answer[j+1] = '1'
        elif newJ == 4:
            answer[j] = '-'
            answer[j+1] = '1'
        elif newJ == 5:
            answer[j] = '0'
            answer[j+1] = '1'
        else:
            raise Exception("unexpected")
        decimal -= x
        decimal //= 5
        j += 1
    
    answer = "".join(reversed(answer)).lstrip("0")
    return answer

file = open('day25input.txt', 'r')
data = [line.strip() for line in file.readlines()]

time0 = time.perf_counter()
answer = 0
for line in data:
    answer += snafuToDecimal(line)
answer = decimalToSnafu(answer)
print("Part 1 Answer = " + str(answer))
time1 = time.perf_counter()
print(f"Done in {time1 - time0:0.4f} seconds")