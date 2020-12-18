from functools import reduce

INPUT = "input.txt"


with open(INPUT, "r") as f:
    TARGET = int(f.readline())

    TIMES = [int(time) if time != "x" else None
             for time in f.readline().strip().split(",")]


best = min((((time - (TARGET % time)) % time, time)
            for time in TIMES if time is not None), key=lambda p: p[0])

print(best[0] * best[1])

def ExtendedEuclid(x, y):
    x0, x1, y0, y1 = 1, 0, 0, 1

    while y > 0:
        q, x, y = x // y, y, x % y
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1

    return 1, x0, y0  # gcd and the two coefficients

def invmod(a, m):
	g, x, y = ExtendedEuclid(a, m)
	if g != 1:
	    raise ValueError('modular inverse does not exist')
	else:
	    return x % m


def ChineseRemainderGauss(eqs):
    result = 0
    N = reduce(lambda acc, eq: acc * eq[1], eqs, 1)

    for a, n in eqs:
        b = N // n

        result += a * b * invmod(b, n)

    return result % N

eqs = [(-t[0],t[1]) for t in enumerate(TIMES) if t[1] is not None]

print(ChineseRemainderGauss(eqs))
