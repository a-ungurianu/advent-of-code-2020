from queue import Queue
from collections import defaultdict
from functools import reduce


def reverse_edge(edge):
    if edge.startswith("R"):
        return edge[1:]
    return "R" + edge


def rot_right(square):
    return square[3], square[0], square[1], square[2]


def flip_v(square):
    return reverse_edge(square[0]), square[3], reverse_edge(square[2]), square[1]


def flip_h(square):
    return square[2], reverse_edge(square[1]), square[0], reverse_edge(square[3])


OPS = [rot_right, flip_v, flip_h]


visited = set()

OG_SQUARE = ("N", "E", "S", "W")

to_check = Queue()
to_check.put(OG_SQUARE)

while not to_check.empty():
    square = to_check.get()
    visited.add(square)

    for op in OPS:
        new_square = op(square)
        if new_square not in visited:
            to_check.put(new_square)


INPUT = "input.txt"


def parse_image(image):
    iden, rest = image.split(":")
    tile_id = int(iden[4:])

    image = rest.strip().split("\n")

    return tile_id, image


def get_w_column(image):
    return "".join(row[0] for row in image)


def get_e_column(image):
    return "".join(row[-1] for row in image)


EDGE_GETTERS = {
    "N": lambda image: image[0],
    "S": lambda image: image[-1],
    "W": get_w_column,
    "E": get_e_column
}

for key in list(EDGE_GETTERS.keys()):
    def reversed_func(func):
        return lambda image: func(image)[::-1]
    EDGE_GETTERS["R" +
                 key] = reversed_func(EDGE_GETTERS[key])


def extract_edges_from_image(image):
    for key, getter in EDGE_GETTERS.items():
        yield (key, getter(image))


def extract_edges(images):
    edge_to_tile_id = defaultdict(list)
    tile_id_to_edges = defaultdict(list)
    for tile_id, image in images:
        for loc, edge in extract_edges_from_image(image):
            edge_to_tile_id[edge].append((tile_id, loc))
            tile_id_to_edges[tile_id].append((edge, loc))
    return edge_to_tile_id, tile_id_to_edges


with open(INPUT, "r") as f:
    data = "".join(f.readlines())
    images = [parse_image(image) for image in data.split("\n\n")]

edge_to_tile_id, tile_id_to_edges = extract_edges(images)

unmatched_edges_ids = []
for tile_id, edges in tile_id_to_edges.items():
    unmatched_edges = 0
    for edge, loc in edges:
        if len(edge_to_tile_id[edge]) == 1:
            unmatched_edges += 1

    if unmatched_edges == 4:
        unmatched_edges_ids.append(tile_id)
        print(tile_id, unmatched_edges)

print(reduce(lambda a, b: a*b, unmatched_edges_ids))
