from collections import namedtuple
from functools import reduce


Rule = namedtuple("Rule", "name first_interval second_interval")


def parse_rule(rule_line):
    name, rest = rule_line.split(": ")

    first_interval, second_interval = rest.split(" or ")

    f_a, f_b = [int(v) for v in first_interval.split("-")]
    s_a, s_b = [int(v) for v in second_interval.split("-")]

    return Rule(name, (f_a, f_b), (s_a, s_b))


def match_rule(rule, value):
    f_a, f_b = rule.first_interval
    s_a, s_b = rule.second_interval

    return f_a <= value <= f_b or s_a <= value <= s_b


INPUT = "input.txt"


with open(INPUT, "r") as f:
    RULES = []
    while (line := f.readline().strip()) != "":
        RULES.append(parse_rule(line))

    assert f.readline().strip().startswith("your ")

    MY_TICKET = [int(val) for val in f.readline().strip().split(",")]
    f.readline()
    assert f.readline().strip().startswith("nearby")

    OTHER_TICKETS = []
    for line in f.readlines():
        OTHER_TICKETS.append([int(val) for val in line.strip().split(",")])


def is_ticket_valid(ticket, rules):
    for value in ticket:
        if not any(match_rule(rule, value) for rule in rules):
            return False
    return True


def get_bad_values(tickets, rules):
    for ticket in tickets:
        for value in ticket:
            is_ok = any(match_rule(rule, value) for rule in rules)
            if not is_ok:
                yield value


print(sum(get_bad_values(OTHER_TICKETS, RULES)))

VALID_TICKETS = [
    ticket for ticket in OTHER_TICKETS if is_ticket_valid(ticket, RULES)] + [MY_TICKET]

transposed = list(zip(*VALID_TICKETS))


POSSIBLE_FIELD_NAMES = []

for field in transposed:
    possible_field_names = set()
    for rule in RULES:
        if all(match_rule(rule, value) for value in field):
            possible_field_names.add(rule.name)
    POSSIBLE_FIELD_NAMES.append(possible_field_names)

final_names = {}


def find_first_single_option(fields):
    for idx, names in enumerate(POSSIBLE_FIELD_NAMES):
        if len(names) == 1:
            return (idx, next(iter(names)))


while True:
    result = find_first_single_option(POSSIBLE_FIELD_NAMES)
    if result is None:
        break
    idx, name = result
    final_names[idx] = name

    for fields in POSSIBLE_FIELD_NAMES:
        fields.discard(name)

print(final_names)


vals = []
for key, value in final_names.items():
    if value.startswith("departure"):
        vals.append(MY_TICKET[key])

print(reduce(lambda a, b: a*b, vals, 1))
