from math import sin, cos, radians

from collections import namedtuple

#      N
#    W + E
#      S


def rotate(d, theta):
    x, y = d
    st = sin(radians(theta))
    ct = cos(radians(theta))

    return (
        x * ct - y * st,
        x * st + y * ct
    )


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def muls(a, scalar):
    return (a[0] * scalar, a[1] * scalar)


def rotate_around(point, around, theta):
    translated = sub(point, around)

    rotated = rotate(translated, theta)

    return add(rotated, around)


def parse_step(line):
    return (line[0], int(line[1:]))


State = namedtuple("State", "pos direction")

DIRECTIONS = {
    "N": (0, 1),
    "S": (0, -1),
    "E": (1, 0),
    "W": (-1, 0)
}


def step(state, step):
    typ, amount = step

    if typ in DIRECTIONS:
        return State(add(state.pos, muls(DIRECTIONS[typ], amount)), state.direction)

    if typ == "F":
        return State(add(state.pos, muls(state.direction, amount)), state.direction)

    rot_dir = 1 if typ == "L" else -1

    return State(state.pos, rotate(state.direction, amount * rot_dir))


def step_with_waypoint(state, step):
    typ, amount = step

    if typ in DIRECTIONS:
        return State(state.pos, add(state.direction, muls(DIRECTIONS[typ], amount)))

    if typ == "F":
        return State(add(state.pos, muls(state.direction, amount)), state.direction)

    rot_dir = 1 if typ == "L" else -1

    return State(state.pos, rotate(state.direction, amount * rot_dir))


INPUT = "input.txt"

with open(INPUT, "r") as f:
    STEPS = [parse_step(line.strip()) for line in f.readlines()]


cur = State((0, 0), (1, 0))

for s in STEPS:
    cur = step(cur, s)
    print(cur)

pos = cur.pos

print(abs(pos[0])+abs(pos[1]))


cur = State((0, 0), (10, 1))


for s in STEPS:
    cur = step_with_waypoint(cur, s)
    print(cur)

pos = cur.pos

print(abs(pos[0])+abs(pos[1]))
