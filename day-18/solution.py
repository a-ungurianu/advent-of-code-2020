import re

TOKENS = {
    "LP": r"\(",
    "RP": r"\)",
    "N": r"\d+",
    "O": r"\+|\*"
}

TOKENS_RE = re.compile(
    "|".join(f"(?P<{token}>{reg})" for token, reg in TOKENS.items()))

PREC = {
    "+": 2,
    "*": 1
}


def tokenize_expression(line):
    tokens = []
    for match in TOKENS_RE.finditer(line):
        for key in TOKENS.keys():
            val = match.groupdict()[key]
            if val is not None:
                tokens.append((key, val))
    return tokens


def to_polish_notation(tokens):
    output = []
    operators = []
    for token in tokens:
        t, val = token

        if t == "N":
            output.append(token)
        elif t == "O":
            while operators and operators[-1][0] != "LP":
                t_top, v_top = operators[-1]
                if t_top != "LP" and PREC[v_top] >= PREC[val]:
                    output.append(operators.pop())
                else:
                    break
            operators.append(token)
        elif t == "LP":
            operators.append(token)
        elif t == "RP":
            while operators[-1][0] != "LP":
                output.append(operators.pop())
            operators.pop()
    while operators:
        output.append(operators.pop())

    return output


OP_EVAL = {
    "+": lambda a, b: a + b,
    "*": lambda a, b: a * b
}


def eval_polish(tokens):

    numbers = []

    for token in tokens:
        t, val = token
        if t == "N":
            numbers.append(int(val))
        elif t == "O":
            numbers.append(OP_EVAL[val](numbers.pop(), numbers.pop()))

    assert len(numbers) == 1
    return numbers[0]


INPUT = "input.txt"

with open(INPUT, "r") as f:
    EXPRESSIONS = [tokenize_expression(line.strip()) for line in f.readlines()]


print(sum(eval_polish(to_polish_notation(expr)) for expr in EXPRESSIONS))
