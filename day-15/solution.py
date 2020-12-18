
INPUT = "input.txt"

with open(INPUT, "r") as f:
    START = [int(n) for n in f.readline().split(",")]


last_seen = {}
for idx, num in enumerate(START[:-1]):
    last_seen[num] = idx

print(last_seen)
last = START[-1]

step = 3000000
target = 0

for idx in range(len(START), 30000000):
    next_last = (idx-1) - last_seen[last] if last in last_seen else 0
    last_seen[last] = idx-1
    last = next_last
    if idx >= target:
        print(target)
        target += step

print(last)
