
INPUT = "input.txt"


with open(INPUT, "r") as f:
    MAP = [line.strip() for line in f.readlines()]

W = len(MAP[0])
H = len(MAP)

STEP = (3,1)


def move(current, step):
    return ((current[0] + step[0]) % W, current[1] + step[1])

def get_tree_count(slope):

    cur = (0,0)
    tree_count = 0

    while cur[1] < H:
        if MAP[cur[1]][cur[0]] == "#":
            tree_count+=1
        cur = move(cur,slope)
    return tree_count

def get_tree_count_product(slopes):
    product = 1
    for count in map(get_tree_count,slopes):
        product *= count
    return product

PART_1_SLOPES = [(3,1)]
PART_2_SLOPES = [(1,1),(3,1), (5,1),(7,1),(1,2)]


print(get_tree_count_product(PART_1_SLOPES))
print(get_tree_count_product(PART_2_SLOPES))
