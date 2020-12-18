import re
from collections import defaultdict
from queue import Queue

PARENT_BAG_NAME = r"^(?P<parent_bag_name>\w+ \w+) bags?"
BAG_NAME = r"((?P<count>\d+) (?P<bag_name>\w+ \w+) bags?(, )?)"


INPUT = "input.txt"

with open(INPUT, "r") as f:
    RULES = [line.strip() for line in f.readlines()]


CAN_CONTAIN = {}
CAN_BE_CONTAINED_IN = defaultdict(list)


for rule in RULES:
    parent = re.match(PARENT_BAG_NAME, rule)
    parent_name = parent.group("parent_bag_name")

    children = [(find.group("bag_name"),int(find.group("count"))) for find in re.finditer(BAG_NAME, rule)]
    CAN_CONTAIN[parent_name] = children
    for child in children:
        CAN_BE_CONTAINED_IN[child[0]].append(parent_name)


START_BAG = "shiny gold"

visited = set()
queue = Queue()
queue.put(START_BAG)

while not queue.empty():
    bag = queue.get()
    visited.add(bag)
    
    for parent in CAN_BE_CONTAINED_IN[bag]:
        queue.put(parent)

print(len(visited) - 1)

def total_bags(bag):
    total = 1
    for child_bag in CAN_CONTAIN[bag]:
        child_bag_name, child_bag_count = child_bag
        total += child_bag_count * total_bags(child_bag_name)
    return total

print(total_bags(START_BAG) - 1)
