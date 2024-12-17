from modules.data_processor import get_puzzle_input


def solve_part_1(input_data: str) -> str:
    # Parse input
    lines = input_data.strip().split('\n')

    # Get register values
    registers = {'A': 0, 'B': 0, 'C': 0}
    for line in lines:
        if line.startswith('Register'):
            reg, val = line.split(': ')
            registers[reg[-1]] = int(val)

    # Get program
    for line in lines:
        if line.startswith('Program:'):
            program = [int(x) for x in line.split(': ')[1].split(',')]
            break

    output = []
    ip = 0  # instruction pointer

    while ip < len(program) - 1:
        opcode = program[ip]
        operand = program[ip + 1]

        if opcode == 0:  # adv
            power = get_combo_value(operand, registers)
            registers['A'] //= (1 << power)
            ip += 2
        elif opcode == 1:  # bxl
            registers['B'] ^= operand
            ip += 2
        elif opcode == 2:  # bst
            registers['B'] = get_combo_value(operand, registers) % 8
            ip += 2
        elif opcode == 3:  # jnz
            if registers['A'] != 0:
                ip = operand
            else:
                ip += 2
        elif opcode == 4:  # bxc
            registers['B'] ^= registers['C']
            ip += 2
        elif opcode == 5:  # out
            val = get_combo_value(operand, registers) % 8
            output.append(str(val))
            ip += 2
        elif opcode == 6:  # bdv
            power = get_combo_value(operand, registers)
            registers['B'] = registers['A'] // (1 << power)
            ip += 2
        elif opcode == 7:  # cdv
            power = get_combo_value(operand, registers)
            registers['C'] = registers['A'] // (1 << power)
            ip += 2

    return ','.join(output)


def get_combo_value(operand: int, registers: dict) -> int:
    if operand <= 3:
        return operand
    elif operand == 4:
        return registers['A']
    elif operand == 5:
        return registers['B']
    elif operand == 6:
        return registers['C']
    return 0  # operand 7 is reserved


def solve_part_2(input_str):
    pass


if __name__ == '__main__':
    day = 17
    data = get_puzzle_input(day=day)

    result_part_1 = solve_part_1(data)
    print(f"Puzzle result part 1: {result_part_1}")

    result_part_2 = solve_part_2(data)
    print(f"Puzzle result part 2: {result_part_2}")
