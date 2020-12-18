from collections import Counter

INPUT = "input.txt"

with open(INPUT, "r") as f:
    GROUPS = [[]]
    for line in f.readlines():
        if line.strip() == "":
            GROUPS.append([])
        else:
            GROUPS[-1].append(line.strip())


def questions_anyone_answered_in_group(group):
    counter = Counter()

    for answers in group:
        counter.update(Counter(answers))

    return counter.keys()


def questions_everyone_answered_in_group(group):
    counter = Counter()

    for answers in group:
        counter.update(Counter(answers))

    return [key for key in counter.keys() if counter[key] == len(group)]


print(sum(map(len, map(questions_anyone_answered_in_group, GROUPS))))
print(sum(map(len, map(questions_everyone_answered_in_group, GROUPS))))
