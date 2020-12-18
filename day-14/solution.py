import re


INPUT = "input.txt"


def apply_mask(number,mask):
    result = 0
    
    for m,n in zip(mask, number):
        if m is not None:
            n = m
        result = (result << 1) | n

    return result

def parse_mask(line):
    return [int(c) if c != 'X' else None for c in line]

def spread_number(line:str):
    return [int(c) for c in line.rjust(36, '0')]


UPDATE_MASK = "UPDATE_MASK"
SET_MEMORY = "SET_MEMORY"

UPDATE_MASK_RE = re.compile(r"mask = (?P<mask>[01X]{36})")
SET_MEMORY_RE = re.compile(r"mem\[(?P<index>\d+)\] = (?P<value>\d+)" )

def parse_op(line):
    line = line.strip()

    match = UPDATE_MASK_RE.match(line)
    if match:
        mask = match.group("mask")
        return (UPDATE_MASK, parse_mask(mask))
    
    match = SET_MEMORY_RE.match(line)
    if match:
        idx = int(match.group("index"))
        value = int(match.group("value"))
        value_spread = spread_number(bin(value)[2:])

        return (SET_MEMORY, idx, value_spread)

def spread_to_number(spread):
    result = 0

    for bit in spread:
        result = (result << 1) | bit
    
    return result

def _gen_addresses(remaining, address_prefix):
    if not remaining:
        yield spread_to_number(address_prefix)
        return

    bit, mask = remaining[0]

    if mask == 0:
        yield from _gen_addresses(remaining[1:], address_prefix + [bit])
    elif mask == 1:
        yield from _gen_addresses(remaining[1:], address_prefix + [1])
    else:
        yield from _gen_addresses(remaining[1:], address_prefix + [1])
        yield from _gen_addresses(remaining[1:], address_prefix + [0])


        

def gen_addresses(address, mask):
    return _gen_addresses(list(zip(address, mask)), [])


with open(INPUT, "r") as f:
    OPS = [parse_op(line) for line in f.readlines()]


mem = {}
mask = [None]*36

for op in OPS:
    typ = op[0]

    if typ == UPDATE_MASK:
        mask = op[1]
    
    if typ == SET_MEMORY:
        index = op[1]
        value = op[2]
        mem[index] = apply_mask(value, mask)

print(sum(mem.values()))


mem = {}
mask = [0]*36

for op in OPS:
    typ = op[0]

    if typ == UPDATE_MASK:
        mask = op[1]
    
    if typ == SET_MEMORY:
        index = op[1]
        value = op[2]
        
        for address in gen_addresses(spread_number(bin(index)[2:]),mask):
            mem[address] = spread_to_number(value)

print(sum(mem.values()))
