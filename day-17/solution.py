from collections import namedtuple, defaultdict

Point = namedtuple("Point", "x y z w")

RANGE = [-1, 0, 1]


def get_3d_neighbours(point):
    for dx in RANGE:
        for dy in RANGE:
            for dz in RANGE:
                if not(dx == 0 and dy == 0 and dz == 0):
                    yield Point(point.x + dx, point.y + dy, point.z + dz, 0)


def get_4d_neighbours(point):
    for dx in RANGE:
        for dy in RANGE:
            for dz in RANGE:
                for dw in RANGE:
                    if not(dx == 0 and dy == 0 and dz == 0 and dw == 0):
                        yield Point(point.x + dx, point.y + dy, point.z + dz, point.w + dw)


def step_universe(universe: defaultdict, neighbour_getter):
    neighbour_count = defaultdict(int)

    for pos, activity in universe.items():
        for neigh in neighbour_getter(pos):
            if activity == ACTIVE:
                neighbour_count[neigh] += 1

    new_universe = defaultdict(lambda: INACTIVE)

    for pos, count in neighbour_count.items():
        activity = universe[pos]

        if activity == ACTIVE:
            if 2 <= count <= 3:
                new_universe[pos] = ACTIVE
        else:
            if count == 3:
                new_universe[pos] = ACTIVE

    return new_universe


INPUT = "input.txt"

ACTIVE = "#"
INACTIVE = "."

START_STATE = defaultdict(lambda: INACTIVE)

with open(INPUT, "r") as f:
    for x, line in enumerate(f.readlines()):
        for y, c in enumerate(line.strip()):
            if c == ACTIVE:
                START_STATE[Point(x, y, 0, 0)] = ACTIVE


universe = START_STATE

for _ in range(6):
    universe = step_universe(universe, get_3d_neighbours)

print(sum(1 if val == ACTIVE else 0 for val in universe.values()))


universe = START_STATE

for _ in range(6):
    universe = step_universe(universe, get_4d_neighbours)

print(sum(1 if val == ACTIVE else 0 for val in universe.values()))
