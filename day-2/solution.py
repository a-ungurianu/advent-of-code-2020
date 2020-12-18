from collections import Counter

INPUT = "input.txt"

def extract_task(line):
    constraint, password = line.split(": ")

    length, letter = constraint.split(" ")
    start, end = length.split("-")

    return (int(start),int(end),letter,password)


def sled_check_task(task):
    start, end, letter, password = task
    counts = Counter(password)
    return start <= counts[letter] <= end

def tobbogan_check_task(task):
    start, end, letter, password = task

    letters = password[start - 1] + password[end - 1]
    count = Counter(letters)

    return count[letter] == 1

with open(INPUT, "r") as f:
    tasks = [extract_task(line) for line in f.readlines()]

print(len([None for task in tasks if sled_check_task(task)]))
print(len([None for task in tasks if tobbogan_check_task(task)]))

