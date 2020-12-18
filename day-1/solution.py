import bisect

INPUT = "input.txt"

TARGET = 2020

numbers = []

with open(INPUT, "r") as f:
    for line in f.readlines():
        numbers.append(int(line))

numbers = sorted(numbers)

for number in numbers:
    insertion_point = bisect.bisect(numbers, TARGET-number) - 1
    if(number + numbers[insertion_point] == TARGET):
        print(number * numbers[insertion_point])
        break

for i in range(len(numbers)):
    for j in range(i+1, len(numbers)):
        a,b = numbers[i], numbers[j]
        insertion_point = bisect.bisect(numbers, TARGET-a-b) - 1
        if(a + b + numbers[insertion_point] == TARGET):
            print(a * b * numbers[insertion_point])
            break
