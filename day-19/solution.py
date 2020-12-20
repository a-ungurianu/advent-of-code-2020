from functools import partial
from operator import itemgetter


def parse_rule(line):

    idx_s, rest = line.split(":")
    idx = int(idx_s)

    options = [[component[1:-1] if component.startswith('"') else int(
        component) for component in option.split(" ")] for option in rest.strip().split(" | ")]

    return idx, options


def matches_rules(rules, line):

    def matches_component(line, component):
        if type(component) == str:
            if line and line[0] == component:
                return True, line[1:]
            else:
                return False, line
        else:
            return matches_rule(line, rules[component])

    def matches_rule(line, rule):
        for option in rule:
            matches, rest = matches_option(line, option)
            if matches:
                return True, rest
        return False, line

    def matches_option(line, option):
        rest = line
        for comp in option:
            matches, rest = matches_component(rest, comp)
            if not matches:
                return False, line

        return True, rest

    matches, rem = matches_rule(line, rules[0])

    return matches and rem == ""


INPUT = "input.txt"

with open(INPUT, "r") as f:
    RULES = {}
    while (line := f.readline().strip()) != "":
        idx, rule = parse_rule(line)
        RULES[idx] = rule

    INPUTS = [line.strip() for line in f.readlines()]


print(sum(1 if matches_rules(RULES, line) else 0 for line in INPUTS))
