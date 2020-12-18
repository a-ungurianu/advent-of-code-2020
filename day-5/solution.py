from itertools import zip_longest

INPUT = "input.txt"


def seat_to_id(seat):
    seat = seat.replace("F", "0")
    seat = seat.replace("B", "1")
    seat = seat.replace("R", "1")
    seat = seat.replace("L", "0")

    return int(seat, base=2)


with open(INPUT, "r") as f:
    seats = [line.strip() for line in f.readlines()]

ids = sorted([seat_to_id(seat) for seat in seats])

for neighs in zip(ids, ids[1:]):
    a, b = neighs

    if b - a != 1:
        print(neighs)
