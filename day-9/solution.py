import bisect

from timeit import default_timer as timer

INPUT = "input.txt"
PREAMBLE_SIZE = 25

def is_valid_number(preamble, number):
    sorted_preamble = sorted(preamble)

    for a in sorted_preamble:
        b_idx = bisect.bisect(sorted_preamble, number-a) - 1
        if number - a  == sorted_preamble[b_idx]:
            return True
    
    return False

def find_first_wrong(numbers, preamble_size):
    for idx in range(len(numbers) - preamble_size):
        if not is_valid_number(numbers[idx:idx + preamble_size], numbers[idx + preamble_size]):
            return numbers[idx + preamble_size]
    return None

def find_contigous(numbers, number):
    running_sum = 0
    left, right = 0, 0

    while True:
        if running_sum < number:
            running_sum += numbers[right]
            right += 1
        elif running_sum > number:
            running_sum -= numbers[left]
            left += 1
        else:
            return numbers[left:right]


with open(INPUT, "r") as f:
    NUMBERS = [int(line) for line in f.readlines()]

first_wrong = find_first_wrong(NUMBERS, PREAMBLE_SIZE)
print(first_wrong)

contiguous_range = find_contigous(NUMBERS, first_wrong)

print(min(contiguous_range) + max(contiguous_range))
