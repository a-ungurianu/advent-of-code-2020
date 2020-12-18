from collections import Counter

from functools import lru_cache

INPUT = "input.txt"

with open(INPUT, "r") as f:
    ADAPTERS = [int(line) for line in f.readlines()]


sorted_adapters = sorted(ADAPTERS)

all_devices = [0] + sorted_adapters + [sorted_adapters[-1] + 3]

differences = Counter(map(lambda pair:pair[1] - pair[0], zip(all_devices, all_devices[1:])))

print(differences[1] * differences[3])


reversed_devices = list(reversed(all_devices))


@lru_cache(maxsize=None)
def arrangement_count(target, device_idx):
    if device_idx >= len(reversed_devices)-1:
        return 1
    total = 0
    while device_idx < len(reversed_devices):
        adapter = reversed_devices[device_idx]
        if target - adapter <= 3:
            total += arrangement_count(adapter, device_idx+1)
        device_idx += 1
    
    return total


print(arrangement_count(reversed_devices[0], 1))

