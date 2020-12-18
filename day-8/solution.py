from collections import namedtuple

INPUT="input.txt"

def extract_instruction(line):
    instruction, value = line.split(" ")

    return (instruction, int(value))

with open(INPUT, "r") as f:
    PROGRAM = [extract_instruction(line) for line in f.readlines()]

State = namedtuple("State", "instruction_pointer accumulator")

INSTRUCTIONS = {
    "acc": lambda state, value: State(state.instruction_pointer + 1, state.accumulator + value),
    "nop": lambda state, value: State(state.instruction_pointer + 1, state.accumulator),
    "jmp": lambda state, value: State(state.instruction_pointer + value, state.accumulator)
}

def does_it_terminate(program):
    state = State(0,0)

    seen_instructions = set()

    while 0 <= state.instruction_pointer < len(program):
        if state.instruction_pointer in seen_instructions:
            return (False, state.accumulator)
        seen_instructions.add(state.instruction_pointer)
        instruction, value = program[state.instruction_pointer]
        state = INSTRUCTIONS[instruction](state, value)
    
    return (True, state.accumulator)


INSTRUCTIONS_SWAP = {
    "nop": "jmp",
    "jmp": "nop"
}

def get_terminting_acc_value(program):
    for idx, line in enumerate(program):
        instruction, value = line

        if instruction in INSTRUCTIONS_SWAP:
            swapped_instruction = INSTRUCTIONS_SWAP[instruction]
            patched_program = program[:idx] + [(swapped_instruction, value)] + program[idx+1:]
            terminates, final_acc = does_it_terminate(patched_program)
            if terminates:
                return final_acc


print(does_it_terminate(PROGRAM)[1])
print(get_terminting_acc_value(PROGRAM))
