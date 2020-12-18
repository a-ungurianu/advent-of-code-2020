
import re

from functools import partial

INPUT = "input.txt"


REQUIRED = [
    "byr",
    "iyr",
    "eyr",
    "hgt",
    "hcl",
    "ecl",
    "pid",
]

digits4 = re.compile(r"^\d{4}$")
digits9 = re.compile(r"^\d{9}$")
haircolor = re.compile(r"^#[0-9a-f]{6}$")
height = re.compile(r"^(\d+)(in|cm)$")

EYE_COLORS = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]

def height_validator(val):
    match = height.match(val)
    
    if match is None:
        return False

    amount = int(match.group(1))
    unit = match.group(2)

    if unit == "cm":
        return 150 <= amount <= 193
    elif unit == "in":
        return 59 <= amount <= 76
    return False
    

VALIDATORS = {
    "byr": lambda val: digits4.match(val) and (1920 <= int(val) <= 2002),
    "iyr": lambda val: digits4.match(val) and (2010 <= int(val) <= 2020),
    "eyr": lambda val: digits4.match(val) and (2020 <= int(val) <= 2030),
    "hgt": height_validator,
    "hcl": lambda val: bool(haircolor.match(val)),
    "ecl": lambda val: val in EYE_COLORS,
    "pid": lambda val: bool(digits9.match(val)),
}

def extract_line_data(line):
    entries = line.split(" ")

    data = {}
    for entry in entries:
        key,value = entry.split(":")
        data[key] = value
    return data


def extract_block_data(block):
    data = {}
    for line in block:
        data.update(extract_line_data(line.strip()))
    return data

def is_passport_valid(use_validators, passport):
    for key in REQUIRED:
        if key not in passport or (use_validators and not VALIDATORS[key](passport[key])):
            return False
    return True

with open(INPUT, "r") as f:
    BLOCKS = [[]]
    for line in f.readlines():
        if line == "\n":
            BLOCKS.append([])
        else:
            BLOCKS[-1].append(line)


print(len(list(filter(partial(is_passport_valid, False), map(extract_block_data, BLOCKS)))))
print(len(list(filter(partial(is_passport_valid, True), map(extract_block_data, BLOCKS)))))

