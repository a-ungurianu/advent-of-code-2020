
INPUT = "input.txt"

EMPTY = "L"
BUSY = "#"
NO_SEAT = "."


def get_map_size(seats):
    return (len(seats), len(seats[0]))


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


NEIGHBOURS = [(dx, dy) for dx in [-1, 0, 1]
              for dy in [-1, 0, 1] if dx != 0 or dy != 0]


class SeatMap:

    def __init__(self, initial_map, line_of_sight=False):
        self.current_map = initial_map
        self.size = get_map_size(self.current_map)
        self.line_of_sight = line_of_sight

    def get_pos(self, pos):
        return self.current_map[pos[0]][pos[1]]

    def is_valid_pos(self, pos):
        row, col = pos
        row_count, col_count = self.size

        return 0 <= row < row_count and 0 <= col < col_count

    def get_seat_in_direction(self, pos, dp):
        if self.line_of_sight:
            return self.get_next_los_seat(pos, dp)
        else:
            return self.get_next_seat(pos, dp)

    def get_next_seat(self, pos, dp):
        nxt = add(pos, dp)
        if self.is_valid_pos(nxt):
            return self.get_pos(nxt)
        return EMPTY

    def get_next_los_seat(self, pos, dp):
        cur = add(pos, dp)
        while self.is_valid_pos(cur):
            seat = self.get_pos(cur)
            if seat != NO_SEAT:
                return seat

            cur = add(cur, dp)

        return EMPTY

    def get_occupied_neighbours(self, pos):
        total = 0
        for dp in NEIGHBOURS:
            nxt = self.get_seat_in_direction(pos, dp)
            total += 1 if nxt == BUSY else 0

        return total

    def next_square_state(self, pos):
        curr_seat = self.get_pos(pos)
        if curr_seat == NO_SEAT:
            return NO_SEAT

        occupied_count = self.get_occupied_neighbours(pos)
        if curr_seat == BUSY:
            return EMPTY if occupied_count >= (5 if self.line_of_sight else 4) else BUSY

        if curr_seat == EMPTY:
            return BUSY if occupied_count == 0 else EMPTY

    def step_map(self):
        new_seats = []
        row_count, col_count = self.size

        for row in range(row_count):
            new_seats.append([])
            for col in range(col_count):
                new_seats[row].append(self.next_square_state((row, col)))

        return SeatMap(new_seats)

    def find_steady_state(self):
        curr_map = self
        while True:
            next_seats = curr_map.step_map()
            if curr_map == next_seats:
                return curr_map
            curr_map = next_seats

    def __eq__(self, oth):
        for row1, row2 in zip(self.current_map, oth.current_map):
            for cell1, cell2 in zip(row1, row2):
                if cell1 != cell2:
                    return False

        return True

    def __str__(self):
        return "\n".join(["".join(row) for row in self.current_map]) + "\n"

    def count_occupied(self):
        return sum(1 if cell == BUSY else 0 for row in self.current_map for cell in row)


with open(INPUT, "r") as f:
    START_MAP = [list(line.strip()) for line in f.readlines()]


simple_sim = SeatMap(START_MAP)

print(simple_sim.find_steady_state().count_occupied())

los_sim = SeatMap(START_MAP, line_of_sight=True)

print(los_sim.find_steady_state().count_occupied())
